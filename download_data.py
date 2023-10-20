from ftplib import FTP
from tqdm import tqdm
from pathlib import Path
from dotenv import dotenv_values

if __name__ == "__main__":
    config = dotenv_values()
    ftp = FTP("genome.leibniz-fli.de")
    login_response = ftp.login(user=config['FLI_FTP_USER'], passwd=config['FLI_FTP_PASSWORD'])

    dataset_names = ['20211028_688_KLR/2022',
                     '20210520_644_MB',
                     '20201014_582_KLR/ATAC',
                     '20201014_582_KLR/GEX']

    local_data_folder = Path('/cellfile/datapublic/jkoubele/leibniz_institute_data')

    for dataset in dataset_names:
        remote_file_paths = ftp.nlst(f'/data/{dataset}')
        dataset_size = sum([ftp.size(file) for file in remote_file_paths])
        print(f"Downloading dataset {dataset} (size: {round(dataset_size / 1e9, 3)} GB)")
        (local_data_folder / dataset).mkdir(exist_ok=True, parents=True)
        for file_path in tqdm(remote_file_paths, desc=f'Downloading {dataset}'):
            with open(local_data_folder / dataset / file_path.split('/')[-1], 'wb') as file:
                ftp.retrbinary(f'RETR {file_path}', file.write)
