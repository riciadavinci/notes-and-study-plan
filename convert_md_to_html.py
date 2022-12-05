# imports
import markdown
import os
import shutil

def check_ignore_list(filepath):
    IGNORE_LIST = [".git/", "venv/", "build/", ".git\\", "venv\\", "build\\"]
    for subpath in IGNORE_LIST:
        if subpath in filepath:
            return False
    return True

def check_if_markdown_file(filepath):
    _, extension = os.path.splitext(filepath)
    MD_EXTENSION = ".md"
    if extension == MD_EXTENSION:
        return True
    return False

def find_md_files(startpath):
    markdown_files = []
    for idx, (root, dirs, files) in enumerate(os.walk(startpath), start=1):
        filepaths = map(lambda f: os.path.join(root, f), files)
        non_ignored_files = filter(check_ignore_list, filepaths)
        markdown_files +=  list(filter(check_if_markdown_file, non_ignored_files))
    return markdown_files

def mk_outfilepath(BASEPATH, filepath):
    updated_basepath = os.path.join(BASEPATH, "docs")
    updated_basename, _ = os.path.split(os.path.join(updated_basepath, filepath.replace(BASEPATH, "")[1:]))
    outfilepath = os.path.join(updated_basename, "index.html")
    return outfilepath

def check_if_img_dir(dirpath):
    TARGET_DIRNAME = "img"
    _, dirname = os.path.split(dirpath)
    if dirname == TARGET_DIRNAME:
        return True
    return False

def find_img_dirs(startpath):
    img_dirs = []
    for root, dirs, files in os.walk(startpath):
        dirpaths = map(lambda d: os.path.join(root, d), dirs)
        non_ignored_dirs = filter(check_ignore_list, dirpaths)
        img_dirpaths = filter(check_if_img_dir, non_ignored_dirs)
        img_dirs +=  list(img_dirpaths)
    return img_dirs

def mk_docs_outdir_path(BASEPATH, filepath):
    updated_basepath = os.path.join(BASEPATH, "docs")
    out_dirpath = os.path.join(updated_basepath, filepath.replace(BASEPATH, "")[1:])
    return out_dirpath

def copy_img_dirs_to_docs(src, dst):
    if not os.path.exists(src):
        return
    shutil.copytree(src, dst)
    print("Copied images to : {}".format(dst))

def convert_to_md(in_filepath, out_filepath):
    if not os.path.exists(in_filepath):
        return
    os.makedirs(os.path.dirname(out_filepath), exist_ok=True)
    with open(in_filepath, "r") as ifp, open(out_filepath, "w") as ofp:
        md_text = ifp.read()
        html_text = markdown.markdown(md_text)
        ofp.write(html_text)
        print("Created: {}".format(out_filepath))

def main():
    CWD = os.getcwd()
    DOCS_DIR = os.path.join(CWD, "docs")
    if os.path.exists(DOCS_DIR):
        shutil.rmtree(DOCS_DIR)
    os.makedirs(DOCS_DIR, exist_ok=True)
    markdown_files = find_md_files(CWD)
    in_out_files = map(lambda in_file: (in_file, mk_outfilepath(CWD, in_file)), markdown_files)
    list(map(lambda file_tuple: convert_to_md(file_tuple[0], file_tuple[1]), in_out_files))
    img_dirs = find_img_dirs(CWD)
    in_out_img_dirs = map(lambda in_dir: (in_dir, mk_docs_outdir_path(CWD, in_dir)), img_dirs)
    list(map(lambda img_dir_tuple: copy_img_dirs_to_docs(img_dir_tuple[0], img_dir_tuple[1]), in_out_img_dirs))


if __name__ == "__main__":
    main()

