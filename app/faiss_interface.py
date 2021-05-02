import faiss


class SingletonFaiss:
    __faiss_index = None

    def __init__(self, path, embedding_size):
        """ Virtually private constructor. """
        self.path = path
        self.embedding_size = embedding_size

        if SingletonFaiss.__faiss_index is None:
            SingletonFaiss.__faiss_index = faiss.read_index(path)

    def search(self, query_vector, topk):
        similarities, indexs = (
            SingletonFaiss
            .__faiss_index
            .search(query_vector.reshape(-1, self.embedding_size), topk)
        )
        return similarities[0], indexs[0]

    def insert(self, vector):
        (
            SingletonFaiss
            .__faiss_index.add(vector.reshape(-1, self.embedding_size))
        )

    def save_index(self):
        faiss.write_index(SingletonFaiss.__faiss_index, self.path)
