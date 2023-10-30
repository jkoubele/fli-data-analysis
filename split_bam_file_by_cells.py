from pathlib import Path

import pandas as pd
import pysam
from tqdm import tqdm


def split_bam_file_by_cell_barcodes(bam_file_path: Path,
                                    cell_barcodes: set[str],
                                    output_folder: Path) -> None:
    """
    Split .bam file to multiple smaller ones, each containing reads from a single cell.
    :param bam_file_path: Path to a .bam file with reads.
    :param cell_barcodes: Set of cell barcodes. Reads with barcodes not present in cell_barcodes will be ignored.
    :param output_folder: Folder to which the resulting files will be written.
    :return: None.
    """
    output_folder.mkdir(parents=True, exist_ok=True)
    samfile_input = pysam.AlignmentFile(bam_file_path, "rb")
    output_file_names_by_barcode = {barcode: output_folder / f"{barcode}.bam" for barcode in cell_barcodes}
    output_samfiles_by_barcode = {barcode: pysam.AlignmentFile(file_path, "wb",
                                                               template=samfile_input)
                                  for barcode, file_path in output_file_names_by_barcode.items()}
    for read in tqdm(samfile_input, desc=f'Processing reads from the input .bam file {bam_file_path}'):
        if not (read.has_tag('CB') and read.has_tag('UB') and read.get_tag('UB') != '-'):
            continue

        read_barcode = read.get_tag('CB')
        if read_barcode in cell_barcodes:
            output_samfiles_by_barcode[read_barcode].write(read)

    for samfile_output in output_samfiles_by_barcode.values():
        samfile_output.close()
    for file_name in tqdm(output_file_names_by_barcode.values(), desc='Indexing .bam files'):
        pysam.index(str(file_name))


def split_star_solo_output_by_cell_barcodes(star_solo_output_path: Path,
                                            output_folder_path: Path) -> None:
    barcodes_df = pd.read_csv(
        star_solo_output_path / Path('Solo.out/GeneFull/filtered/barcodes.tsv'),
        delimiter='\t',
        names=['barcode'])
    split_bam_file_by_cell_barcodes(
        bam_file_path=star_solo_output_path / 'Aligned.sortedByCoord.out.bam',
        cell_barcodes=set(barcodes_df['barcode']),
        output_folder=output_folder_path / star_solo_output_path.name)


if __name__ == "__main__":
    for folder in Path(
            '/cellfile/datapublic/jkoubele/leibniz_institute_data/aligned/20201014_582_KLR/GEX').iterdir():
        split_star_solo_output_by_cell_barcodes(star_solo_output_path=folder,
                                                output_folder_path=Path(
                                                    '/cellfile/datapublic/jkoubele/leibniz_institute_data/splitted_by_cells/20201014_582_KLR/GEX/'))
