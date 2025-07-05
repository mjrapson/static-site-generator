import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_htmlnode(self):
        node = HTMLNode("p", "Header 1", None, None)

        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Header 1")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr(self):
        node = HTMLNode("p", "Header 1", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.__repr__(), "Tag: p Value: Header 1 Children: None Props: {'href': 'https://www.google.com', 'target': '_blank'}")