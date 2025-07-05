import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(
            TextNode("This is a text node", TextType.BOLD), 
            TextNode("This is a text node", TextType.BOLD)
        )
        
        self.assertEqual(
            TextNode("This is a text node", TextType.BOLD, "testurl"),
            TextNode("This is a text node", TextType.BOLD, "testurl")
        )

    def test_not_eq(self):
        self.assertNotEqual(
            TextNode("This is a text node", TextType.BOLD), 
            TextNode("This is a text node", TextType.ITALIC)
        )

        self.assertNotEqual(
            TextNode("A", TextType.BOLD),
            TextNode("B", TextType.BOLD)
        )

        self.assertNotEqual(
            TextNode("A", TextType.BOLD),
            TextNode("A", TextType.BOLD, "url")
        )

if __name__ == "__main__":
    unittest.main()