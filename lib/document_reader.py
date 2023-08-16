from langchain.document_loaders import PyPDFLoader

loader = PyPDFLoader("example/Ethereum_Whitepaper_-_Buterin_2014.pdf")
pages = loader.load_and_split()


def document_reader():
    print(pages[0])
