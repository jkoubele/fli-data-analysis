from itertools import chain
from pathlib import Path
import streamlit as st

from error_detection import CellErrorStatistics

detected_errors_data_folder_path = Path(
    '/cellfile/datapublic/jkoubele/leibniz_institute_data/computed_errors/20201014_582_KLR/GEX')


def load_available_datasets() -> list[str]:
    return [folder.name for folder in detected_errors_data_folder_path.iterdir() if folder.is_dir()]


@st.cache_data
def load_cell_error_statistics(dataset_name: str) -> list[CellErrorStatistics]:
    cell_error_statistics: list[CellErrorStatistics] = []
    c = 0
    for file_path in (detected_errors_data_folder_path / dataset_name).iterdir():
        with open(file_path) as file:
            cell_error_statistics.append(CellErrorStatistics.from_json(file.read()))
        c += 1
        if c % 100 == 0:
            print(c)
    return cell_error_statistics


def inverted_value_string(original_value: float) -> str:
    return f"$~~~$(inverted value: *{round(1 / original_value, 2)}*)" if original_value > 0 else f"$~~~$(inverted value: *NaN*)"


def display_dataset_level_statistics(dataset_name: str) -> None:
    cell_error_statistics = load_cell_error_statistics(dataset_name=dataset_name)
    with st.expander("Dataset overview", expanded=True):
        st.markdown("##### Coverage")
        st.markdown(f"Number of cells (barcodes): **{len(cell_error_statistics)}**")
        num_detected_nucleotides = sum(
            [cell_statistics.num_consensus_reads_total for cell_statistics in cell_error_statistics])
        st.markdown(f"Total number of detected nucleotides: **{'{:.3g}'.format(num_detected_nucleotides)}**")
        num_covered_positions = sum(
            [cell_statistics.num_positions_with_sufficient_coverage for cell_statistics in cell_error_statistics])
        st.markdown(f"Total number of covered positions: **{'{:.3g}'.format(num_covered_positions)}**")
        st.markdown("##### Transcription Errors")
        transcription_errors = list(
            chain.from_iterable([cell_statistics.transcription_errors for cell_statistics in cell_error_statistics]))
        num_transcription_errors = len(transcription_errors)
        st.markdown(f"Number of detected transcription errors: **{num_transcription_errors}**")
        st.markdown(
            f"Transcription error rate (per nucleotide): **{'{:.3e}'.format(num_transcription_errors / num_detected_nucleotides)}**" + inverted_value_string(
                num_transcription_errors / num_detected_nucleotides))
        st.markdown(
            f"Transcription error rate (per position): **{'{:.3e}'.format(num_transcription_errors / num_covered_positions)}**" + inverted_value_string(
                num_transcription_errors / num_covered_positions))

        st.markdown("##### Mutations")
        mutation_errors = list(
            chain.from_iterable([cell_statistics.mutation_errors for cell_statistics in cell_error_statistics]))
        num_mutations = len(mutation_errors)
        st.markdown(f"Number of detected mutations: **{num_mutations}**")
        st.markdown(
            f"Mutation rate (per position): **{'{:.3e}'.format(num_mutations / num_covered_positions)}**" + inverted_value_string(
                num_mutations / num_covered_positions))


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    available_datasets = load_available_datasets()
    mode_radio_options = ['Single dataset exploration', 'Two dataset comparison']
    mode_radio = st.radio("Mode", mode_radio_options)
    if mode_radio == mode_radio_options[0]:
        dataset_name_1 = st.selectbox('Select dataset', available_datasets, key='selectbox 1')
        display_dataset_level_statistics(dataset_name_1)
    elif mode_radio == mode_radio_options[1]:
        column_1, column_2 = st.columns(2)
        with column_1:
            dataset_name_1 = st.selectbox('Select dataset', available_datasets, key='selectbox 1')
            display_dataset_level_statistics(dataset_name_1)
        with column_2:
            dataset_name = st.selectbox('Select dataset', available_datasets, key='selectbox 2')
            display_dataset_level_statistics(dataset_name)
