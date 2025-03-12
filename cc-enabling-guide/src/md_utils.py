import re
import os
from src.constants import *
import subprocess
from urllib.parse import urlparse

def extract_code_blocks(markdown_text):
    """
    Extract code blocks from the given markdown text.
    
    Args:
        markdown_text (str): Markdown text to extract code blocks from.
    
    Returns:
        list: List of code blocks.
    """
    code_blocks = re.findall(r'```(.*?)```', markdown_text, re.DOTALL)
    return code_blocks

def read_markdown_file(file_path):
    """
    Read the content of a markdown file.
    
    Args:
        file_path (str): Path to the markdown file.
    
    Returns:
        str: Content of the markdown file.
    """
    with open(file_path, 'r') as file:
        return file.read()

def extract_fragment_from_url(url):
    """
    Extract the fragment part from a URL.
    
    Args:
        url (str): URL to extract the fragment from.
    
    Returns:
        str: Extracted fragment.
    """
    parsed_url = urlparse(url)
    return re.sub(r'\d-', '', parsed_url.fragment)

def extract_code_block_from_sh(file_path, start_marker, end_marker):
    """
    Extract a code block from a shell script file between specified markers.
    
    Args:
        file_path (str): Path to the shell script file.
        start_marker (str): Start marker for the code block.
        end_marker (str): End marker for the code block.
    
    Returns:
        str: Extracted code block or None if not found.
    """
    with open(file_path, 'r') as file:
        content = file.read()
    
    pattern = re.compile(re.escape(start_marker) + r'(.*?)' + re.escape(end_marker), re.DOTALL)
    match = pattern.search(content)
    
    if match:
        return match.group(1).strip()
    else:
        return None

def replace_substrings(command, replacements):
    for old, new in replacements.items():
        command = command.replace(old, new)
    return command

def extract_code_blocks_after_text(markdown_text, search_text, markdown_type, distro=None):
    """
    Extract code blocks that appear after a specific search text in the markdown text.
    
    Args:
        markdown_text (str): Markdown text to search in.
        search_text (str): Text to search for.
        markdown_type (str): Type of markdown (single_command, multi_distro, etc.).
        distro (str, optional): Distribution name. Defaults to None.
    
    Returns:
        list or str: Extracted code blocks or the first code block if markdown_type is not multi_distro.
    """
    print(f"Search text: {search_text}")
    print(f"Distro: {distro}")
    search_position = markdown_text.find(search_text)
    if search_position == -1:
        return []  # Return an empty list if the search text is not found
    text_after_search = markdown_text[search_position + len(search_text):]
    code_blocks = extract_code_blocks(text_after_search)
    if markdown_type != "multi_distro" and markdown_type != "read_from_other_file":
        return code_blocks[0] if code_blocks else None  # Return the first code block if found 
    else:
        if distro == "CentOS Stream 9":
            return code_blocks[0]
        elif distro == "Ubuntu 24.04":
            return code_blocks[1]
        elif distro == "OpenSuse 15.3":
            return code_blocks[2]
        else:
            return None

def extract_links(markdown_text):
    """
    Extract links from the given markdown text.
    
    Args:
        markdown_text (str): Markdown text to extract links from.
    
    Returns:
        list: List of tuples containing link text and URL.
    """
    link_pattern = re.compile(r'\[([^\]]+)\]\((http[^\)]+)\)')
    links = link_pattern.findall(markdown_text)
    return links

def extract_links_with_text(markdown_text, search_text):
    """
    Extract links that contain the search text in the link text or URL.
    
    Args:
        markdown_text (str): Markdown text to search in.
        search_text (str): Text to search for in the links.
    
    Returns:
        list: List of filtered links.
    """
    links = extract_links(markdown_text)
    filtered_links = [link for link in links if search_text in link[0] or search_text in link[1]]
    return filtered_links

def extract_version_from_url(url):
    """
    Extract the version number from a URL.
    
    Args:
        url (str): URL to extract the version number from.
    
    Returns:
        str: Extracted version number or None if not found.
    """
    pattern = re.compile(r'/tree/([\d\.]+)')
    match = pattern.search(url)
    if match:
        return match.group(1)
    return None

def extract_commands_from_link(markdown_string, distro, url, markdown_type):
    """
    Extract commands from a link in the markdown string.
    
    Args:
        markdown_string (str): Markdown string to extract commands from.
        distro (str): Distribution name.
        url (str): URL to extract commands from.
        markdown_type (str): Type of markdown (single_command, multi_distro, etc.).
    
    Returns:
        dict: Dictionary of commands and their verifier strings.
    """
    command_verifier_strings = {}

    if distro == "Ubuntu 24.04":
        page_section = extract_fragment_from_url(url)
        page_section = page_section.replace("-","_")
        branch = extract_version_from_url(url)
        checkout_repo(canonical_repo, branch)
        canonical_readme_text = read_markdown_file(canonical_readme_path)
        search_list = f"canonical_{page_section}"
        print(f"Search list: {eval(search_list)}")
        for items in eval(search_list):
            verifier_string = items.split(":")[1]
            search_string = items.split(":")[0]
            command = extract_code_blocks_after_text(canonical_readme_text, search_string, markdown_type, distro)
            print(f"\ncommand: {command}")
            pattern = re.compile(r'\{.*?\}')
            cleaned_text = pattern.sub('', command).strip()
            print(f"#########\nMarkdown string: {markdown_string}")
            command_verifier_strings[cleaned_text]=verifier_string
    else:
        checkout_repo(sig_centos_repo, sig_centos_branch)
        if "tdx/host" in url:
            sig_centos_text = read_markdown_file(sig_centos_host_os_path)
            command_list = f"sig_host"
        else:
            sig_centos_text = read_markdown_file(sig_centos_guest_os_path)
            page_section = extract_fragment_from_url(url)
            page_section = page_section.replace("-","_")
            command_list = f"sig_{page_section}"
        for items in eval(command_list):
            command = extract_code_blocks_after_text(sig_centos_text, items, markdown_type, distro)
            pattern = re.compile(r'\{.*?\}')
            cleaned_text = pattern.sub('', command).strip()
            print(f"#########\nMarkdown string: {markdown_string}")
    return command_verifier_strings

def checkout_repo(repo_url, branch_name):
    """
    Clone the specified repository and checkout the specified branch.
    
    Args:
        repo_url (str): URL of the repository to clone.
        branch_name (str): Branch name to checkout.
    """
    print(f"\n\nGit clone repo: {repo_url}")
    print(f"Git checkout branch: {branch_name}")
    subprocess.run(["git", "clone", repo_url], cwd=workspace_path)
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    subprocess.run(["git", "checkout", branch_name], cwd=os.path.join(workspace_path,repo_name))
