import argparse
import concurrent.futures
import io

from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes
import pypdf
import requests


VALID_PAPERS = {f"2P{no}" for no in range(1, 9)}

VALID_YEARS = set(range(1996, 2024))
VALID_YEARS.remove(2020)


def parse_question_paper(paper_input: str):
    if ":" in paper_input:
        paper_year, page_selections = paper_input.split(":")

        pages: list[int] = list()
        for page_selection in page_selections.split(","):
            if "-" in page_selection:  # "3-5"
                first_page, last_page = page_selection.split("-")
                # Zero-indexed page numbers
                pages.extend(range(int(first_page) - 1, int(last_page)))
            else:  # "3"
                # Zero-indexed page numbers
                pages.append(int(page_selection) - 1)

    else:
        paper_year = paper_input
        pages = None

    paper, year = paper_year.split("_")
    return paper, int(year), pages


def get_download_url(paper: str, year: int) -> str:
    if paper not in VALID_PAPERS:
        raise ValueError(f"Invalid paper: {paper}, must be one of {VALID_PAPERS}")

    if year not in VALID_YEARS:
        raise ValueError(f"Invalid year: {year}, must be one of {VALID_YEARS}")

    return f"https://cribs-static.vercel.app/IB/tripos/{paper}/QP_{year}.pdf"


def get_file(url: str):
    response = requests.get(url)
    pdf_bytes_reader = io.BytesIO(response.content)
    return pypdf.PdfReader(pdf_bytes_reader)


def get_text_pdf(text: str):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=pagesizes.A4)
    width, height = pagesizes.A4

    can.setFont("Times-Roman", 20)
    can.drawString(50, height - 50, text)

    can.save()
    packet.seek(0)  # Reset to start of file

    return pypdf.PdfReader(packet).get_page(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("question_papers", nargs="+", type=str,
                        help="Question papers in form <paper>_<year> with optional page number selections."
                        " e.g. 2P3_2003 2P4_2014:5,7-9")
    parser.add_argument("-o", "--output", default="output.pdf",
                        type=str, help="File name for the combined pdf")
    parser.add_argument("-w", "--watermark", action="store_true",
                        help="If set, will watermark each file with "
                        "the paper name and year in the top left corner")

    args = parser.parse_args()

    output_pdf = pypdf.PdfWriter()

    papers, years, page_lists = zip(*[parse_question_paper(question_paper_arg) for question_paper_arg
                                      in args.question_papers])
    urls = [get_download_url(paper, year) for paper, year in zip(papers, years)]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        qp_pdfs = executor.map(get_file, urls)

    prev_len = 0
    for paper, year, pages, qp_pdf in zip(papers, years, page_lists, qp_pdfs):
        output_pdf.append(qp_pdf, pages=pages)

        page_len = output_pdf.get_num_pages()

        if args.watermark:
            watermark_page = get_text_pdf(f"{paper} {year}")
            for page_no in range(prev_len, page_len):
                output_pdf.get_page(page_no).merge_page(watermark_page)

        prev_len = page_len

    output_pdf.write(args.output)


if __name__ == "__main__":
    main()
