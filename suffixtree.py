class SuffixTree(object):
    def __init__(self, word):
        self._word = word
        self._root = _Node()
        self._insert(word)

    def suffixes(self):
        stack = [(self._root, '')]
        while stack:
            node, prefix = stack.pop()
            for edge in node._edges.itervalues():
                new_prefix = prefix + self._word[edge.start:edge.end]
                if edge.target:
                    stack.append((edge.target, new_prefix))

                else:
                    yield new_prefix

    def __contains__(self, other):
        current_node = self._root
        current_edge = None
        current_length = 0

        for char in other:
            if current_node is None:
                return False
            if current_node == self._root:
                if char not in current_node._edges:
                    return False
                current_length = 1
                current_edge = char
            else:
                edge_data = current_node._edges[current_edge]
                if self._word[edge_data.start + current_length] != char:
                    return False
                current_length += 1
                if edge_data.start + current_length == edge_data.end:
                    current_node = edge_data.target

        return True

    def _insert(self, word):
        active_node = self._root
        active_edge = None
        active_length = 0
        remainder = 0
        for letter_idx, letter in enumerate(word):
            prev_split = None
            remainder += 1
            while remainder > 0:
                node_has_letter = active_node.has_letter(letter, active_edge,
                                                         active_length, word)
                if not node_has_letter:
                    if active_edge:
                        new_node = active_node.split(active_edge,
                                                     active_length,
                                                     word)
                        new_node.add(letter, letter_idx, None)
                        if prev_split:
                            prev_split.suffix_link = new_node
                        prev_split = new_node
                        if active_node != self._root:
                            if active_node.suffix_link:
                                active_node = active_node.suffix_link
                            else:
                                active_node = self._root
                        else:
                            active_length -= 1
                            if active_length > 0:
                                active_edge = word[letter_idx - remainder + 2]
                            else:
                                active_edge = None
                        remainder -= 1
                    else:
                        assert(active_node == self._root)
                        active_node.add(letter, letter_idx, None)
                        remainder -= 1
                else:
                    if active_edge is None:
                        assert(active_length == 0)
                        active_edge = letter
                        active_length = 1
                        break
                    else:
                        active_length += 1
                        edge_data = active_node.get_edge(active_edge)
                        if edge_data.end is not None:
                            edge_length = edge_data.end - edge_data.start
                            assert(edge_length >= active_length)
                            if active_length == edge_length:
                                active_node = edge_data.target
                                active_length = 0
                                active_edge = None
                        break


class _Node(object):
    def __init__(self):
        self._edges = {}
        self.suffix_link = None

    def has_letter(self, letter, edge_label, idx, word):
        if edge_label is None:
            assert(idx == 0)
            return letter in self._edges
        else:
            assert(idx > 0)
            edge = self._edges[edge_label]
            return word[edge.start + idx] == letter

    def add(self, letter, start, end):
        assert(letter not in self._edges)
        self._edges[letter] = _Edge(start, end, None)

    def split(self, edge_label, length, word):
        edge = self._edges[edge_label]
        assert(edge.end is None)
        assert(edge.target is None)
        edge.end = edge.start + length
        edge.target = _Node()
        edge.target.add(word[edge.end], edge.end, None)
        return edge.target

    def get_edge(self, edge_label):
        return self._edges[edge_label]

    def __repr__(self):
        return "<Node: %s>" % repr(self._edges)


class _Edge(object):
    def __init__(self, start, end, target):
        self.start = start
        self.end = end
        self.target = target

    def __repr__(self):
        return "<Edge: start=%d, end=%s, target=%s>" % (
            self.start, str(self.end), repr(self.target))
