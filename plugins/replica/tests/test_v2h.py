"""[V2H] Testes da casa: o que o catálogo acrescenta ou exige ao replica-skill.

Substituem o test_repo.py do upstream, que verificava a arrumação do repo
original (pastas replica-<x>/ na raiz, README do reel) e não a do catálogo.
"""

import json
import os
import re
import struct
import tempfile
import unittest
import zlib

from _load import load, ROOT

imgdiff = load("replica-diff", "imgdiff")

SKILLS = ["recon", "architect", "design", "build", "backend", "test", "diff",
          "entrepreneur", "brand", "launch", "deploy"]
UPSTREAM_SHA = "77c9436"


def frontmatter(name):
    with open(os.path.join(ROOT, "skills", name, "SKILL.md"), encoding="utf-8") as fh:
        text = fh.read()
    # Bloco dobrado (>-): uma descrição numa linha só com ": " ou aspas parte o YAML,
    # e o Claude Code carrega a skill sem descrição, calado (aconteceu à design:taste).
    m = re.match(r"^---\nname: (.+)\ndescription: >-\n((?:  .+\n)+)---\n", text)
    return m, text


def png(path, w, h, payload):
    def chunk(kind, body):
        return (struct.pack(">I", len(body)) + kind + body +
                struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF))
    data = (imgdiff.SIG + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) +
            chunk(b"IDAT", zlib.compress(payload)) + chunk(b"IEND", b""))
    with open(path, "wb") as fh:
        fh.write(data)


class Catalogo(unittest.TestCase):
    def test_onze_skills_com_o_nome_da_pasta(self):
        found = sorted(d for d in os.listdir(os.path.join(ROOT, "skills"))
                       if os.path.isfile(os.path.join(ROOT, "skills", d, "SKILL.md")))
        self.assertEqual(found, sorted(SKILLS))
        for s in SKILLS:
            m, _ = frontmatter(s)
            self.assertIsNotNone(m, s)
            self.assertEqual(m.group(1), s)

    def test_gatilhos_presos_a_clones(self):
        # O original disparava em "how does X work" e "map out X", em qualquer projeto.
        for s in SKILLS:
            m, _ = frontmatter(s)
            desc = m.group(2)
            self.assertNotRegex(desc.lower(), r"how does|map out|como funciona", s)
            self.assertRegex(desc, r"clon|replica/", s)

    def test_plugin_json_sem_version(self):
        with open(os.path.join(ROOT, ".claude-plugin", "plugin.json"), encoding="utf-8") as fh:
            plugin = json.load(fh)
        self.assertEqual(plugin["name"], "replica")
        self.assertNotIn("version", plugin)

    def test_licenca_mit_e_rodape_em_todas(self):
        with open(os.path.join(ROOT, "LICENSE"), encoding="utf-8") as fh:
            lic = fh.read()
        self.assertIn("MIT License", lic)
        self.assertIn("Jake Schincariol", lic)
        for s in SKILLS:
            _, text = frontmatter(s)
            self.assertIn("## Origem e licença", text, s)
            self.assertIn(UPSTREAM_SHA, text, s)

    def test_nomes_no_formato_do_plugin(self):
        for s in SKILLS:
            _, text = frontmatter(s)
            self.assertNotRegex(text, r"/replica-(?!skill)[a-z]", s)
            self.assertNotIn("../replica-", text, s)

    def test_regra_de_conteudo_de_terceiros(self):
        for s in ("recon", "entrepreneur"):
            _, text = frontmatter(s)
            self.assertIn("[V2H]", text)
            self.assertIn("nunca instrução", text, s)
            self.assertIn("sem conectores", text, s)

    def test_sem_travessoes(self):
        # Regra do upstream, mantida para o corpo não divergir do original.
        bad = []
        for dirpath, dirnames, filenames in os.walk(ROOT):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for fn in filenames:
                if fn.endswith((".md", ".py", ".json", ".ts", ".csv")):
                    path = os.path.join(dirpath, fn)
                    with open(path, encoding="utf-8") as fh:
                        if chr(0x2014) in fh.read():
                            bad.append(os.path.relpath(path, ROOT))
        self.assertEqual(bad, [])


class PngBomba(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def test_dados_a_mais_sao_recusados(self):
        p = os.path.join(self.tmp.name, "bomba.png")
        png(p, 10, 10, b"\0" * 5000000)   # declara 10x10, descomprime para 5 MB
        with self.assertRaises(imgdiff.PngError) as ctx:
            imgdiff.read_png(p)
        self.assertIn("more image data", str(ctx.exception))

    def test_dimensoes_absurdas_sao_recusadas_antes_de_descomprimir(self):
        p = os.path.join(self.tmp.name, "gigante.png")
        png(p, 60000, 60000, b"\0")
        with self.assertRaises(imgdiff.PngError) as ctx:
            imgdiff.read_png(p)
        self.assertIn("megapixel limit", str(ctx.exception))

    def test_png_legitimo_continua_a_abrir(self):
        p = os.path.join(self.tmp.name, "ok.png")
        rows = [[(x * 20, y * 20, 100) for x in range(12)] for y in range(9)]
        imgdiff.write_png(p, 12, 9, rows)
        self.assertEqual(imgdiff.read_png(p), (12, 9, rows))


if __name__ == "__main__":
    unittest.main()
