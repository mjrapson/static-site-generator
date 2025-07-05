import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_node_to_html_div(self):
        node = LeafNode("div", "Some Text")
        self.assertEqual(node.to_html(), "<div>Some Text</div>")

    def test_lead_node_to_html_no_tag(self):
        node = LeafNode(None, "Hello")
        self.assertEqual(node.to_html(), "Hello")

if __name__ == "__main__":
    unittest.main()