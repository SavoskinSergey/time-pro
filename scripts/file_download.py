import requests
import tqdm


def download_files(url: str, filename: str):
    with open(filename, 'wb') as f:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))

            tqdm_params = {
                'desc': url,
                'total': total,
                'miniters': 1,
                'unit': 'it',
                'unit_scale': True,
                'unit_divisor': 1024,
            }

            with tqdm.tqdm(**tqdm_params) as pb:
                for chunk in r.iter_content(chunk_size=8192):
                    pb.update(len(chunk))
                    f.write(chunk)
    pass


def main():

    # url = 'https://www.4sync.com/web/directDownload/WOZq952H/3nR8Q8Hf.2d8d62324e115e9ca9033ac154850bb4'
    url = input("Введите Url:")
    # filename = 'image2.png'
    filename = input('Введите название файла:')
    download_files(url, filename)


if __name__ == '__main__':
    main()
