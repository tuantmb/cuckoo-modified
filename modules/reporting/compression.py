# Copyright (C) 2016 Brad Spengler
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import os
import zipfile

from lib.cuckoo.common.abstracts import Report
from lib.cuckoo.common.exceptions import CuckooReportError

class Compression(Report):
    """Compresses analysis artifacts after processing/signatures are complete for permanent storage."""

    def run(self, results):
        zipmemdump = self.options.get("zipmemdump", False)
        zipprocdump = self.options.get("zipprocdump", False)
        zipmemstrings = self.options.get("zipmemstrings", False)
        zipprocstrings = self.options.get("zipprocstrings", False)

        if "procmemory" in results and results["procmemory"]:
            for proc in results["procmemory"]:
                dmp_path = proc.get("file", None)
                strings_path = proc.get("strings_path", None)
        
                if zipprocdump and dmp_path and dmp_path.endswith(".dmp") and os.path.exists(dmp_path):
                    try:
                        f = zipfile.ZipFile("%s.zip" % (dmp_path), "w")
                        f.write(dmp_path, os.path.basename(dmp_path), zipfile.ZIP_DEFLATED)
                        f.close()
                        os.remove(dmp_path)
                        proc["file"]="%s.zip" % (dmp_path)
                    except Exception as e:
                        raise CuckooReportError("Error creating Process Memory Zip File %s" % e)

                if zipprocstrings and strings_path and strings_path.endswith(".strings") and os.path.exists(strings_path):
                    try:
                        f = zipfile.ZipFile("%s.zip" % (strings_path), "w")
                        f.write(strings_path, os.path.basename(strings_path), zipfile.ZIP_DEFLATED)
                        f.close()
                        os.remove(strings_path)
                        proc["strings_path"] = "%s.zip" % (strings_path) 
                    except Exception as e:
                        raise CuckooReportError("Error creating Process Memory Strings Zip File %s" % e)

        if zipmemdump and self.memory_path and os.path.exists(self.memory_path):
            try:
                f = zipfile.ZipFile("%s.zip" % (self.memory_path), "w", allowZip64=True)
                f.write(self.memory_path, os.path.basename(self.memory_path), zipfile.ZIP_DEFLATED)
                f.close()
                os.remove(self.memory_path)
            except Exception as e:
                 raise CuckooReportError("Error creating Full Memory Zip File %s" % e)

        if zipmemstrings and self.memory_path and os.path.exists(self.memory_path + ".strings"):
            strings_path = self.memory_path + ".strings"
            try:
                f = zipfile.ZipFile("%s.zip" % (strings_path), "w", allowZip64=True)
                f.write(strings_path, os.path.basename(strings_path), zipfile.ZIP_DEFLATED)
                f.close()
                os.remove(strings_path)
                strings_path = "%s.zip" % (strings_path)
            except Exception as e:
                raise CuckooReportError("Error creating Full Memory Strings Zip File %s" % e)


