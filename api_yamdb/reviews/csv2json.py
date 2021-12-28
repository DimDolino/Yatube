import csv
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = 'static/data'
FIXTURES_DIR = os.path.join(BASE_DIR, 'reviews/fixtures')
PATH_FILE_IN = os.path.join(BASE_DIR, STATIC_DIR)

DATABASE = {
    'titles': 'Title',
    'category': 'Category',
    'genre_title': 'GenreTitle',
    'genre': 'Genre',
    'review': 'Review',
    'users': 'User',
    'comments': 'Comment',
}


def from_csv_to_json():
    entries = []
    filename = FIXTURES_DIR
    if not os.path.exists(filename):
        os.mkdir(filename)
    file_out = 'fixtures.json'
    out_file = os.path.join(filename, file_out)
    for key in DATABASE:
        in_file = f'{key}.csv'
        in_path = os.path.join(PATH_FILE_IN, in_file)
        model_name = f'reviews.{DATABASE[key]}'
        with open(in_path, encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=",")
            for row in reader:
                fields = {}
                data = {}
                pk = row['id']
                data['id'] = int(pk)
                data["model"] = model_name
                for key in reader.fieldnames:
                    try:
                        fields.update(
                            {
                                key: int(row[key])
                            }
                        )
                    except ValueError:
                        fields.update({
                            key: row[key]
                        })
                    data["fields"] = fields
                entries.append(data)
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(entries, indent=4))


if __name__ == "__main__":
    from_csv_to_json()
