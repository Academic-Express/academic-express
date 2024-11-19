from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from datetime import datetime

from .models import ArxivEntry

# Create your tests here.


class PubTests(APITestCase):
    client: APIClient

    def setUp(self) -> None:
        self.test_arxiv_entry_data = {
            'arxiv_id': '1706.03762v7',
            'authors': [{'name': 'Ashish Vaswani'},
                        {'name': 'Noam Shazeer'},
                        {'name': 'Niki Parmar'},
                        {'name': 'Jakob Uszkoreit'},
                        {'name': 'Llion Jones'},
                        {'name': 'Aidan N. Gomez'},
                        {'name': 'Lukasz Kaiser'},
                        {'name': 'Illia Polosukhin'}],
            'categories': ['cs.CL', 'cs.LG'],
            'comment': '15 pages, 5 figures',
            'link': 'http://arxiv.org/abs/1706.03762v7',
            'pdf': 'http://arxiv.org/pdf/1706.03762v7',
            'primary_category': 'cs.CL',
            'published': '2017-06-12T17:57:34Z',
            'summary': 'The dominant sequence transduction models are based on complex '
            'recurrent or convolutional neural networks in an encoder-decoder '
            'configuration. The best performing models also connect the '
            'encoder and decoder through an attention mechanism. We propose a '
            'new simple network architecture, the Transformer, based solely on '
            'attention mechanisms, dispensing with recurrence and convolutions '
            'entirely. Experiments on two machine translation tasks show these '
            'models to be superior in quality while being more parallelizable '
            'and requiring significantly less time to train. Our model '
            'achieves 28.4 BLEU on the WMT 2014 English-to-German translation '
            'task, improving over the existing best results, including '
            'ensembles by over 2 BLEU. On the WMT 2014 English-to-French '
            'translation task, our model establishes a new single-model '
            'state-of-the-art BLEU score of 41.8 after training for 3.5 days '
            'on eight GPUs, a small fraction of the training costs of the best '
            'models from the literature. We show that the Transformer '
            'generalizes well to other tasks by applying it successfully to '
            'English constituency parsing both with large and limited training '
            'data.',
            'title': 'Attention Is All You Need',
            'updated': '2023-08-02T00:41:18Z'
        }
        self.test_arxiv_entry = ArxivEntry.objects.create(**self.test_arxiv_entry_data)

    def test_get_arxiv_entry(self):
        url = reverse('pub:get_arxiv_entry', kwargs={'arxiv_id': self.test_arxiv_entry_data['arxiv_id']})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for k, v in self.test_arxiv_entry_data.items():
            if k in ('published', 'updated'):
                expected = datetime.fromisoformat(v)
                actual = datetime.fromisoformat(response.data[k])
                self.assertEqual(expected, actual)
            else:
                self.assertEqual(response.data[k], v)
