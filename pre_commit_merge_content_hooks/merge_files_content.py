import argparse
import os
import sys
from pathlib import Path


class Check:
    quiet: bool
    directory: str
    file_pattern: str
    output_filename: str

    def __init__(
        self,
        quiet: bool,
        directory: str,
        output_dir: str,
        file_pattern: str,
        output_filename: str,
    ):
        self.quiet = quiet
        self.directory = directory
        self.file_pattern = file_pattern
        self.output_filename = os.path.join(output_dir, output_filename)

        if not self.quiet:
            sys.stdout.write(
                f"Run with args: \n"
                f"`directory`: {self.directory},\n"
                f"`output_dir`: {output_dir},\n"
                f"`file_pattern`: {self.file_pattern},\n"
                f"`output_filename`: {self.output_filename}\n"
            )

    def get_files_to_process(self) -> list[Path]:
        try:
            filenames = sorted(
                [p for p in Path(self.directory).rglob(self.file_pattern)],
                key=lambda p: str(p.parent / p.name)
            )
        except Exception:
            raise Exception("Can't get list of files to process. Incorrect filename pattern.\n")

        if not filenames:
            raise Exception("Can't get list of files to process. No files found.\n")

        return filenames

    def get_old_content(self) -> str:
        if not os.path.isfile(self.output_filename):
            return ""

        with open(self.output_filename) as f:
            return f.read()

    @classmethod
    def get_merged_content(cls, files: list[Path]) -> str:
        contents = []
        for filename in files:
            if not os.path.isfile(filename):
                raise Exception(f"File {filename} was not found.\n")

            with open(filename) as f:
                content = f.read()
                if not content:
                    raise Exception(f"File {filename} is empty.\n")
                contents.append(content)

        return "\n\n\n".join(contents) + "\n"

    def _execute(self):
        """Read content from all files found in `directory` and its subdirs and merge it to file `output_filename`

        Parameters
        ----------
        directory : string
          Path to directory storing all files to merge

        output_dir : string
          Path where merged file will be created

        file_pattern : string
          Pattern of filenames

        output_filename : string
          Name of the merged file

        quiet : bool, optional
          Enabled, don't print output to stderr.

        Returns
        -------

        int: 0 if no changes were made, 1 otherwise.
        """

        new_content = self.get_merged_content(files=self.get_files_to_process())
        old_content = self.get_old_content()

        if old_content == new_content:
            return 0

        with open(self.output_filename, 'w') as outfile:
            outfile.write(new_content)

        return 1

    def execute(self):
        try:
            return self._execute()
        except Exception as e:
            sys.stderr.write(str(e) or f"Hook error happened: {repr(e)}")
            return 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Changed files")

    parser.add_argument("-q", "--quiet", required=False, default=False, help="Supress output")
    parser.add_argument("--dir", required=True, help="Path to directory storing all files to merge")
    parser.add_argument("--file_pattern", required=False, default="*.sql", help="Pattern of filenames")
    parser.add_argument("--output_dir", required=True, help="Path where merged file will be created")
    parser.add_argument("--output_filename", required=True, help="Name of the merged file")

    args = parser.parse_args()

    if not args.filenames:
        return 0

    return Check(
        quiet=args.quiet,
        directory=args.dir,
        output_dir=args.output_dir,
        file_pattern=args.file_pattern,
        output_filename=args.output_filename,
    ).execute()


if __name__ == "__main__":
    exit(main())
