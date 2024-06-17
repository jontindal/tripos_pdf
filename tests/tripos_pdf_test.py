from unittest import mock

import pytest

import tripos_pdf


CONNECTION_ERROR_URL = "https://cribs-stati.vercel.app/IB/tripos/2P1/QP_2023.pdf"
VALUE_ERROR_URL = "https://cribs-static.vercel.app/IB/tripos/2P0/QP_2023.pdf"


@pytest.mark.parametrize("paper", ("1P1", "2P1", "3A1", "4A3"))
def test_parse_question_paper(paper):
    input_str = paper + "_2023"
    assert tripos_pdf.parse_question_paper(input_str) == (paper, 2023, None)


def test_parse_question_paper_pages():
    paper = "1P1"
    input_str = paper + "_2023" + ":3,5-7,1,9-10"
    assert tripos_pdf.parse_question_paper(input_str) == (paper, 2023, [2, 4, 5, 6, 0, 8, 9])


@pytest.mark.parametrize("paper", ("1P1", "2P1", "3A1", "4A3"))
def test_good_url(paper):
    url = tripos_pdf.get_download_url(paper, 2023)
    tripos_pdf.get_file(url)


def test_bad_subdomain_url():
    with pytest.raises(ConnectionError):
        tripos_pdf.get_file(CONNECTION_ERROR_URL)


def test_bad_paper_url():
    with pytest.raises(ValueError):
        tripos_pdf.get_file(VALUE_ERROR_URL)


def test_main_error_propagation(tmp_path):
    with mock.patch.object(tripos_pdf, "get_download_url", lambda paper, year: CONNECTION_ERROR_URL):
        with pytest.raises(ConnectionError):
            output_file = tmp_path / "output.pdf"
            tripos_pdf.main(("2P7_2017", "-o", str(output_file)))


def test_main_single(tmp_path):
    output_file = tmp_path / "output.pdf"
    tripos_pdf.main(("2P7_2017", "-o", str(output_file)))


def test_main_page_selection(tmp_path):
    output_file = tmp_path / "output.pdf"
    tripos_pdf.main(("2P7_2017:3-4,2", "-o", str(output_file)))


def test_main_single_watermarked(tmp_path):
    output_file = tmp_path / "output.pdf"
    tripos_pdf.main(("2P7_2017", "-w", "-o", str(output_file)))


def test_main_multiple(tmp_path):
    output_file = tmp_path / "output.pdf"
    tripos_pdf.main(("1P1_2017", "2P7_2017:3-4,2", "-o", str(output_file)))


def test_main_multiple_watermarked(tmp_path):
    output_file = tmp_path / "output.pdf"
    tripos_pdf.main(("1P1_2017", "2P7_2017:3-4,2", "-w", "-o", str(output_file)))
