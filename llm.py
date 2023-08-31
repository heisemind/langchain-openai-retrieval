from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from documents import Documents
from dotenv import load_dotenv


class LanguageModel:
    def __init__(self) -> None:
        """
        Initialize the LanguageModel class.

        This class sets up the language model for question answering.

        """
        load_dotenv()
        text_splitter = CharacterTextSplitter(
            separator=' ',
            chunk_size=100,
            chunk_overlap=20
        )
        documents = Documents()
        texts = text_splitter.split_text(
            documents.gather_documents())

        embeddings = OpenAIEmbeddings()
        retriever = FAISS.from_texts(texts, embeddings)\
            .as_retriever(search_type='similarity',
                          search_kwargs={'k': 5})

        self.retrieval_qa = RetrievalQA.from_chain_type(
            llm=OpenAI(),
            chain_type='stuff',
            retriever=retriever,
            return_source_documents=True)

    def ask(self, query: str) -> str:
        """
        Answer a question using the language model.

        Args:
            query (str): The question to be answered.

        Returns:
            str: The answer generated by the language model.
        """
        return self.retrieval_qa(query)


if __name__ == '__main__':
    model = LanguageModel()
    print(model.ask('How many parameters does BERT have?'))
