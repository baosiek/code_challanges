from typing import Dict, List


class TrieNode:
    def __init__(
        self,
        character: str,
        is_end_of_word: bool = False
    ):
        self.character = character
        self.children = {}
        self.is_end_of_word = is_end_of_word

    def insert_child(self, char: str):
        if char not in self.children:
            self.children[char] = TrieNode(character=char)

    def get_child(self, char: str) -> 'TrieNode':
        return self.children.get(char)

    def get_children(self) -> Dict[str, 'TrieNode']:
        return self.children

    def children_list(self):
        return self.children.values()

    def delete_child(self, char: str):
        if char in self.children:
            del self.children[char]

    def __str__(self):
        node_string: str = f"{self.character}, " + \
            f"is_end_of_word: {self.is_end_of_word}"
        return node_string


class Trie():
    def __init__(self):
        self.root = TrieNode("root")
        self.size = 0

    def insert_word(
            self,
            word: str
    ):
        stack: List[TrieNode] = [self.root]
        index: int = 0
        while stack and index < len(word):
            node: TrieNode = stack.pop()
            if not node.get_child(word[index]):
                node.insert_child(word[index])
            if index == len(word) - 1:
                node.get_child(word[index]).is_end_of_word = True
                self.size += 1
            stack.append(node.get_child(word[index]))
            index += 1

    def search_word(self, word: str) -> bool:
        node: TrieNode = self.root
        stack: List[TrieNode] = [child for child in reversed(
            node.children_list()
        )]
        index: int = 0

        while stack and index < len(word):
            node = stack.pop()
            if node.character == word[index]:
                if index == len(word) - 1 and node.is_end_of_word:
                    return True
                index += 1
                for child in reversed(node.children_list()):
                    stack.append(child)

        return False

    def delete_word(self, word: str):
        node: TrieNode = self.root
        stack: List[TrieNode] = [child for child in reversed(
            node.children_list()
        )]
        index: int = 0
        backtrack: List[TrieNode] = [self.root]
        found: bool = False

        while stack and index < len(word):
            node = stack.pop()
            if node.character == word[index]:
                backtrack.append(node)
                if index == len(word) - 1 and node.is_end_of_word:
                    node.is_end_of_word = False
                    found = True
                    self.size -= 1
                index += 1
                for child in reversed(node.children_list()):
                    stack.append(child)

        if found:
            child: TrieNode = backtrack.pop()
            while backtrack:
                parent: TrieNode = backtrack.pop()
                if not child.is_end_of_word and len(child.children_list()) \
                        == 0:
                    parent.delete_child(child.character)
                child = parent

    def __str__(self) -> str:
        trie_string: str = ""
        node: TrieNode = self.root
        stack: List[(TrieNode, int)] = [(node, 0)]
        while stack:
            node, level = stack.pop()
            trie_string += f"{'\t' * level}{str(node)}\n"
            for child in reversed(node.children_list()):
                stack.append((child, level + 1))
        return trie_string


if __name__ == '__main__':
    trie = Trie()
    trie.insert_word("car")
    trie.insert_word("cars")
    trie.insert_word("boat")
    trie.insert_word("boats")
    trie.insert_word("race")
    trie.insert_word("races")
    trie.insert_word("boar")
    trie.insert_word("boars")
    trie.insert_word("bond")
    trie.insert_word("bonds")
    trie.insert_word("cloak")
    trie.insert_word("cloaks")
    trie.insert_word("rotten")
    trie.insert_word("tomatoes")
    trie.insert_word("problem")
    trie.insert_word("problems")
    print(str(trie))
    w: str = "problems"
    print(f"Word [{w}] exists: {trie.search_word(w)}")
    trie.delete_word("problems")
    print(f"Word [{w}] exists: {trie.search_word(w)}")
    print(str(trie))
