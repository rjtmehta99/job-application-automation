from __future__ import annotations
import argparse
from cv_resume_generator import constants
from jinja2 import Environment, FileSystemLoader
import pyperclip

def read_args():
    parser = argparse.ArgumentParser(description='Add company and position name')
    parser.add_argument('--company', '-c', help='Company Name')
    parser.add_argument('--position', '-p', help='Position Name')
    parser.add_argument('--domains', '-d', help='Domains', default='')
    args = parser.parse_args()
    company = args.company
    position = args.position
    # Domains like 'finance and e-commerce'
    domains = args.domains
    job_args = {'COMPANY_NAME': company,
                'POSITION': position,
                'DOMAINS': domains}
    return job_args

def render_cover_letter(job_args: dict[str]) -> str:
    env = Environment(loader=FileSystemLoader(constants.DATA_PATH))
    template = env.get_template(constants.COVER_LETTER_PATH)
    rendered_cover_letter = template.render(job_args)
    pyperclip.copy(rendered_cover_letter)
    print('[INFO] Cover letter generated and copied to clipboard.')
    return render_cover_letter
    
if __name__ == '__main__':
    job_args = read_args()
    render_cover_letter(job_args)
