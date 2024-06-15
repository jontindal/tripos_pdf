import pytest

import tripos_pdf


def test_good_url():
    url = tripos_pdf.get_download_url("2P1", 2023)
    tripos_pdf.get_file(url)


def test_bad_subdomain_url():
    with pytest.raises(ConnectionError):
        tripos_pdf.get_file("https://cribs-stati.vercel.app/IB/tripos/2P1/QP_2023.pdf")


def test_bad_paper_url():
    with pytest.raises(ValueError):
        tripos_pdf.get_file("https://cribs-static.vercel.app/IB/tripos/2P0/QP_2023.pdf")
