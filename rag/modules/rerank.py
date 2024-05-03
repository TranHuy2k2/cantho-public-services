from typing import List
from langchain.docstore.document import Document
from langchain_community.document_transformers import (
    LongContextReorder,
)

from app_vars import AppVariables
import tensorflow as tf
from transformers import TFAutoModel, AutoTokenizer
from BERTForClassification import BERTForClassification


class RAGRerank:
    device_name = "/cpu:0"
    with tf.device(device_name):
        model = TFAutoModel.from_pretrained("vinai/phobert-base-v2", from_pt=True)
        tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")
        classifier = BERTForClassification(model, num_classes=2)
        classifier.load_weights('../filter-model/model2/checkpoint/')

    @staticmethod
    def filtering(docs:List[Document], question):
        filtered_docs = []
        with tf.device(RAGRerank.device_name):
            texts = [f'context: {doc.page_content}\nquestion: {question}' for doc in docs]
            tokenized_input = RAGRerank.tokenizer(texts, 
                                        return_tensors="tf", padding=True, truncation=True, max_length=256)
            output = RAGRerank.classifier.call(tokenized_input)
            print(output)
        output = tf.argmax(output, axis=1)
        output = tf.equal(output, 1).numpy().tolist()
        print(output)
        for i in range(len(output)):
            if output[i]:
                filtered_docs.append(docs[i])
        return filtered_docs
        
        
    @staticmethod
    def reranking(docs: List[Document], question):
        results = AppVariables.reranking(
            docs=[doc.page_content for doc in docs],
            question=question
        )
        results = [docs[result.index] for result in results]
        # Reorder to avoid Lost In The Middle
        reordering = LongContextReorder()
        reordered_docs = reordering.transform_documents(results)
        return reordered_docs