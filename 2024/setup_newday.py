import os
import shutil
import sys
import aocd

def create_new_day(day):
    # Define paths
    template_folder = 'dayX'
    new_day_folder = f'day-{day:02d}'

    # Create new day folder
    if not os.path.exists(new_day_folder):
        os.makedirs(new_day_folder)

    # Process files and directories in the template folder
    for root, dirs, files in os.walk(template_folder):
        # Compute the relative path from the template folder
        relative_path = os.path.relpath(root, template_folder)
        target_dir = os.path.join(new_day_folder, relative_path)

        # Create directories in the target location
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        for filename in files:
            template_path = os.path.join(root, filename)
            new_file_path = os.path.join(target_dir, filename)

            # Copy non-template files
            shutil.copy(template_path, new_file_path)

    print(f'New day created: {new_day_folder}')


def downloadDay(day):
    data = aocd.get_data(day=day)
    with open(f'day-{day:02d}/input.txt', 'w') as f:
        f.write(data)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python new-day.py <day>')
        sys.exit(1)

    day = int(sys.argv[1])
    create_new_day(day)
    downloadDay(day)