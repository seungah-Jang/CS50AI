import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob = {}
    linked_pages = corpus[page]
    if linked_pages:
        for p in corpus:            
            if p in linked_pages:
                prob[p] = (1-damping_factor)/len(corpus)+(damping_factor/len(linked_pages))
            else:
                prob[p] = (1-damping_factor)/len(corpus)

        '''
        prob[page] = (1-damping_factor)*(1/len(corpus))
        for p in linked_pages:
            prob[p] = damping_factor*(1/len(linked_pages))
        '''
    else:
        for p in corpus:
            prob[p] = 1/len(corpus)
        #prob[page] = 1/len(corpus)
    return prob

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    import random
    all_pages = list(corpus.keys())
    initial_page = random.choice(all_pages)
    count_pages = {}
    for i in range(len(all_pages)):
        count_pages[all_pages[i]] = 0

    count_pages[initial_page] = 1
    transition_result = transition_model(corpus, initial_page, damping_factor)

    for i in range(n-1):
        current_page = random.choices(list(transition_result.keys()),list(transition_result.values()))[0]
        count_pages[current_page] += 1
        transition_result = transition_model(corpus, current_page, damping_factor)

    for page in count_pages:
        count_pages[page] = count_pages[page] /n
    
    return count_pages


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    all_pages = list(corpus.keys())
    current_pages ={}
    for i in range(len(corpus)):
        current_pages[all_pages[i]] = 1/len(corpus)

    while True:
        new_pages = {}
        for page in all_pages:
            rank_sum = 0
            #역추적
            for linked_page in corpus:
                if page in corpus[linked_page]:
                    rank_sum += (current_pages[linked_page]/len(corpus[linked_page]))
                if len(corpus[linked_page])==0:
                    rank_sum += current_pages[linked_page] / len(all_pages)
            rank_sum *= damping_factor
            rank_sum += (1-damping_factor)/len(corpus)
            new_pages[page] = rank_sum

        flag = True
        for p in new_pages:
            if abs(new_pages[p] - current_pages[p])>0.001:
                flag = False
        if flag == True:
            break
        else:
            current_pages = new_pages

    return current_pages
            

if __name__ == "__main__":
    main()
