from sentence_transformers import SentenceTransformer, util
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"


class ST:
    def __init__(self, qa_pairs_file: str):
        # Read the file with the QA pairs
        with open(qa_pairs_file, "r", encoding="utf-8") as fIn:
            self.qa_pairs = self.create_sets(fIn.read())
            print(self.qa_pairs)

        print("[~] Loading model...")
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.corpus_embeddings = util.normalize_embeddings(
            self.embedder.encode(
                [qa[0] for qa in self.qa_pairs], convert_to_tensor=True
            ).to(device)
        )
        print("[+] Model successfully initialised")

    def create_sets(self, content: str):
        lines = content.strip().split("\n")
        qa_pairs: list[tuple[str, str]] = []
        for line in lines:
            if "-" in line:
                qa = line.split("-")
                question = qa[0].strip()
                answer = qa[1].strip()

                # if the answer is just #, use the previous answer
                if answer.startswith("#"):
                    answer = qa_pairs[-1][1]

                qa_pairs.append((question, answer))
        return qa_pairs

    def search(self, q: str) -> str | None:
        # Encode the question
        q_embed = self.embedder.encode([q], convert_to_tensor=True).to(device)

        # Find possible hits
        hit = util.semantic_search(
            q_embed, self.corpus_embeddings, score_function=util.dot_score, top_k=3
        )[0][0]

        print(hit)

        if hit["score"] < 0.65:
            return None

        return self.qa_pairs[hit["corpus_id"]]
