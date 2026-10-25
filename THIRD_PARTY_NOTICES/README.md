# Third-Party Notices

Len is licensed under GNU GPL version 3. See the `LICENSE` file at the distribution root. The GPL does not replace the licenses and notices for third-party software included in the Windows package.

This directory preserves the upstream license, copyright, and notice text for the controlled Windows packaging inputs recorded in `packaging/third_party_notice_manifest.json`. The text files are copied verbatim from the installed distributions or their matching source distributions, and the release build fails if a required file, hash, runtime version, or package version differs. The October 2026 assessment replaces the Pillow notice with the exact 13.0.0 wheel text; published historical artifacts retain their original notices and bytes.

## Runtime components

| Component | Version | License or status | Notice location |
| --- | --- | --- | --- |
| CPython | 3.12.10 | Python Software Foundation License Version 2 plus the complete incorporated-software license and acknowledgment appendix | `CPython-3.12.10-LICENSE.rst` |
| Tcl/Tk | 8.6.15 | BSD-style Tcl/Tk terms | `Tcl-Tk-8.6-license.terms` |
| PyInstaller bootloader and related files | 6.22.1 | GPL-2.0-or-later with the documented bootloader exception; runtime hooks are Apache-2.0 | `PyInstaller-6.22.1/licenses/COPYING.txt` |
| pandas | 3.0.3 | BSD-3-Clause | `pandas-3.0.3/LICENSE` |
| NumPy and bundled code | 2.5.0 | BSD-3-Clause and the compatible licenses identified by the upstream wheel, including 0BSD, MIT, zlib, CC0-1.0, OpenBLAS/LAPACK, and the GCC runtime exception | `NumPy-2.5.0/` |
| Pillow and embedded image/font libraries | 13.0.0 | MIT-CMU plus the complete upstream wheel inventory for materially embedded libraries, including Brotli, FreeType, HarfBuzz, libavif, libjpeg-turbo, libpng, libtiff, libwebp, Little CMS, OpenJPEG, and zlib | `Pillow-13.0.0/licenses/LICENSE` |
| ReportLab and bundled fonts | 5.0.0 | BSD-style ReportLab license plus the included DarkGarden and Bitstream Vera font notices | `ReportLab-5.0.0/` |
| OpenPyXL | 3.1.5 | MIT | `OpenPyXL-3.1.5/LICENCE.rst` |
| et_xmlfile and incorporated Python code | 2.0.0 | MIT plus applicable Python Software Foundation terms | `et_xmlfile-2.0.0/` |
| python-dateutil | 2.9.0.post0 | Dual Apache-2.0 or BSD-3-Clause | `python-dateutil-2.9.0.post0/LICENSE` |
| six | 1.17.0 | MIT | `six-1.17.0/LICENSE` |
| charset-normalizer | 3.4.7 | MIT | `charset-normalizer-3.4.7/licenses/LICENSE` |
| tzdata / IANA time zone database | 2026.2 | Apache-2.0 for the Python package; IANA database data is public domain as stated by the upstream notice | `tzdata-2026.2/licenses/` |

The distributed CPython runtime contains OpenSSL 3.0.16 and SQLite 3.49.1. Their applicable license/acknowledgment text, including SQLite's public-domain statement, is preserved in CPython's complete incorporated-software appendix rather than paraphrased into a new license. The package also contains Microsoft UCRT 10.0.26100.4654 and VC runtime 14.42.34438 redistributable/system components.

Build-only packages such as `altgraph`, `packaging`, `pefile`, `pyinstaller-hooks-contrib`, `pywin32-ctypes`, and `setuptools` are pinned in `packaging/requirements-release.txt` for build reproducibility. They are not listed as distributed runtime components unless the final package inventory shows that their code is present.

These notices describe third-party terms; they are not legal advice and do not add restrictions to GNU GPL version 3.
