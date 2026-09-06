import argparse
import os
import shutil


def parse_args():
    parser = argparse.ArgumentParser(description="Organize files by type")
    parser.add_argument(
        "source",
        help="Folder to scan and organize"
    )
    parser.add_argument(
        "--base-dir",
        default=os.path.expanduser("~"),
        help="Base directory where Videos/Documents/etc live (default: your real home dir)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would happen without moving anything"
    )
    return parser.parse_args()

args=parse_args()
target_dir=args.source
home_dir = args.base_dir #os.path.expanduser("~")


extensions_dict={
    "Images": [".jpg",".png",".jpeg",".bmp",".gif"],
    "Documents":[".docx",".pdf",".txt",".xlsx",".csv",".ppt"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Music": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".tar", ".rar", ".gz"]
}


def organise_files():
    print(args.source)
    items=os.listdir(target_dir)

    for item in items:
        file_path=os.path.join(target_dir,item)
        if os.path.isdir(file_path):
            continue

        root,file_ext=os.path.splitext(item)
        file_ext = file_ext.lower()

        for category,extensions in extensions_dict.items():
            if file_ext in extensions:
                match category:
                    case "Images":
                        category_dir = os.path.join(home_dir, "Pictures")
                    case "Documents":
                        category_dir = os.path.join(home_dir, "Documents")
                    case "Videos":
                        category_dir = os.path.join(home_dir, "Videos")
                    case "Music":
                        category_dir = os.path.join(home_dir, "Music")
                    case _:
                        continue
                        #category_dir= home_dir

                os.makedirs(category_dir, exist_ok=True)
                dest_path=os.path.join(category_dir, item)

                if args.dry_run:
                    print(f"[DRY RUN] {file_path} -> {dest_path}")
                else:
                    shutil.move(file_path, dest_path)
                print(f"Moved: {item} -> {category}/")
                moved = True
                break

if __name__ == "__main__":
    organise_files()