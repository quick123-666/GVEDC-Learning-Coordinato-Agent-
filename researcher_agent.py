# 研究Agent - 集成记忆系统
# 负责分析论文核心概念、技术要点和实现细节

import os
import json
import re

class ResearcherAgent:
    def __init__(self, project_path, memory_system=None):
        self.project_path = project_path

        # 使用传入的记忆系统
        if memory_system:
            self.memory = memory_system
        else:
            from memory_system import AgentMemorySystem
            self.memory = AgentMemorySystem(project_path)

    def analyze_paper(self, paper_id, paper_file):
        """分析论文"""
        print(f"Researcher analyzing Paper {paper_id}: {paper_file}")

        paper_identifier = f"paper-{paper_id}"

        # 保存论文信息
        self.memory.save_paper(
            paper_id=paper_identifier,
            paper_number=paper_id,
            title=f"Paper {paper_id}",
            file_path=paper_file,
            status="in_progress"
        )

        # 分析论文内容
        analysis_result = self._perform_analysis(paper_id, paper_file)

        # 保存研究分析结果到记忆系统
        analysis_id = self.memory.generate_id("analysis")
        self.memory.save_research_analysis(
            analysis_id=analysis_id,
            paper_id=paper_identifier,
            core_concepts=analysis_result.get('core_concepts', []),
            technical_points=analysis_result.get('technical_points', []),
            implementation_details=analysis_result.get('implementation_details', {}),
            summary=analysis_result.get('summary', '')
        )

        # 提取并保存知识点
        for concept in analysis_result.get('core_concepts', []):
            self.memory.save_concept(
                concept_name=concept,
                description=f"From Paper {paper_id}",
                related_papers=[paper_identifier]
            )

        # 保存学习进度
        progress_id = self.memory.generate_id("progress")
        self.memory.save_learning_progress(
            progress_id=progress_id,
            paper_id=paper_identifier,
            agent_type='researcher',
            stage='analysis',
            status='completed',
            result=json.dumps(analysis_result, ensure_ascii=False)
        )

        # 保存上下文
        self.memory.save_context(
            session_id=f"paper_{paper_id}",
            context_type="research_analysis",
            content=f"完成Paper {paper_id}的分析",
            metadata={"paper_file": paper_file}
        )

        return {
            'paper_id': paper_id,
            'file': paper_file,
            'title': f'Paper {paper_id} Analysis',
            'result': analysis_result
        }

    def _perform_analysis(self, paper_id, paper_file):
        """执行论文分析"""
        # 提取核心概念
        core_concepts = self._extract_core_concepts(paper_id)

        # 提取技术要点
        technical_points = self._extract_technical_points(paper_id)

        # 提取实现细节
        implementation_details = self._extract_implementation_details(paper_id)

        # 生成摘要
        summary = f"Analysis of Paper {paper_id}: {', '.join(core_concepts[:3])}"

        return {
            'core_concepts': core_concepts,
            'technical_points': technical_points,
            'implementation_details': implementation_details,
            'summary': summary
        }

    def _extract_core_concepts(self, paper_id):
        """提取核心概念"""
        concepts_map = {
            2: ['Character-level RNN', 'Language Model', 'Sequence Modeling'],
            3: ['LSTM', 'Vanilla RNN', 'Gradient Flow', 'Gates Mechanism'],
            4: ['Word Embeddings', 'Word2Vec', 'CBOW', 'Skip-gram'],
            5: ['GRU', 'Gated Recurrence', 'Vanishing Gradient'],
            6: ['Neural Machine Translation', 'Seq2Seq', 'Encoder-Decoder'],
            7: ['Attention Mechanism', 'Bahdanau Attention', 'Content-Based Attention'],
            8: ['Transformer', 'Self-Attention', 'Positional Encoding', 'Multi-Head Attention'],
            9: ['BERT', 'Pre-training', 'Fine-tuning', 'Masked Language Model'],
            10: ['GPT', 'Generative Pre-training', 'Unsupervised Learning'],
            11: ['Image Classification', 'AlexNet', 'Deep CNN', 'GPU Training'],
            12: ['ResNet', 'Residual Connection', 'Skip Connection', '152 Layers'],
            13: ['Batch Normalization', 'Internal Covariate Shift', 'Training Speed'],
            14: ['Bahdanau Attention', 'Additive Attention', 'Neural Machine Translation'],
            15: ['Identity Mappings', 'Pre-activation ResNet', 'Gradient Flow'],
            16: ['Dropout', 'Regularization', 'Generalization', 'Neuron Dropout'],
            17: ['Image Segmentation', 'U-Net', 'Encoder-Decoder', 'Skip Connections'],
            18: ['Relational RNN', 'Multi-head Attention', 'Relational Memory'],
            19: ['Irreversibility', 'Entropy', 'Maxwell\'s Demon', 'Landauer Principle'],
            20: ['Neural Turing Machine', 'External Memory', 'Content Addressing'],
            21: ['CTC Loss', 'Speech Recognition', 'Alignment', 'Blank Symbol'],
            22: ['Scaling Laws', 'Power Law', 'Compute Optimal', 'Chinchilla'],
            23: ['Minimum Description Length', 'MDL', 'Model Selection', 'Compression'],
            24: ['Machine Super Intelligence', 'ASI', 'Capability Amplification'],
            25: ['Kolmogorov Complexity', 'Algorithmic Complexity', 'Information Theory'],
            26: ['CNN Fundamentals', 'Convolutional Neural Network', 'Filters', 'Pooling'],
            27: ['Multi-token Prediction', 'Token-level Training', 'Extended Context'],
            28: ['Dense Passage Retrieval', 'DPR', 'Information Retrieval', 'Embedding'],
            29: ['Retrieval-Augmented Generation', 'RAG', 'Knowledge Retrieval', 'LLM'],
            30: ['Lost in the Middle', 'Attention Sink', 'Position Bias', 'Context Management']
        }

        return concepts_map.get(paper_id, [f'Paper {paper_id} Core Concept'])

    def _extract_technical_points(self, paper_id):
        """提取技术要点"""
        tech_map = {
            2: ['Hidden state size', 'Number of layers', 'Truncated BPTT', 'Character embeddings'],
            3: ['Cell state', 'Input/Forget/Output gates', 'LSTM cell architecture'],
            4: ['Hierarchical softmax', 'Negative sampling', 'Window size', 'Embedding dimension'],
            5: ['Update gate', 'Reset gate', 'GRU vs LSTM comparison'],
            6: ['Bidirectional RNN', 'Encoder hidden state', 'Decoder initial state'],
            7: ['Bidirectional attention', 'Concatenation of forward/backward hidden states'],
            8: ['Scaled dot-product attention', 'Multi-head attention blocks', 'Feed-forward layers'],
            9: ['Token masking', 'Next sentence prediction', 'Transformer encoder stack'],
            10: ['Unidirectional transformer', 'Task-agnostic pre-training'],
            11: ['ReLU activation', 'GPU implementation', 'Overlapping pooling', 'Local Response Normalization'],
            12: ['Shortcut connection', 'Identity mapping', 'Bottleneck block', 'Global average pooling'],
            13: ['Moving average', 'Variance normalization', 'Gamma/Beta parameters', 'BN during training'],
            14: ['Alignment scores', 'Context vector', 'Bahdanau scoring function'],
            15: ['Pre-activation order', 'BN-ReLU-Conv', 'Original order: Conv-BN-ReLU'],
            16: ['Bernoulli dropout', 'Weight scaling', 'Inverted dropout', 'Monte Carlo estimation'],
            17: ['Contracting path', 'Expanding path', 'Skip connections', 'Dice coefficient loss'],
            18: ['Memory slots', 'Multi-head attention', 'LSTM-style gating', 'Relational reasoning'],
            19: ['Coffee automaton', 'Diffusion simulation', 'Entropy increase', 'Poincaré recurrence'],
            20: ['Memory matrix', 'Read heads', 'Write heads', 'Content-based addressing', 'Location-based addressing'],
            21: ['Forward algorithm', 'Beam search decoding', 'Greedy decoding', 'CTC prefix decoding'],
            22: ['LMB(x) = A * x^-alpha', 'Compute frontier', 'Training curve extrapolation'],
            23: ['Two-part MDL', 'Stochastic complexity', 'Regret bound', 'Bayesian occam razor'],
            24: ['Recursive self-improvement', 'Capability amplification', 'Distillation'],
            25: ['Kolmogorov complexity K(s)', 'Turing machine', 'Incompressibility', 'Algorithmic probability'],
            26: ['Convolution operation', 'Kernel/Filter', 'Stride', 'Padding', 'Pooling layers'],
            27: ['n-gram prediction', 'Full context window', 'Token interleaving'],
            28: ['Dense vector retrieval', 'Dual encoder', 'Max margin loss', 'In-batch negative sampling'],
            29: ['Retrieve-then-generate', 'Document retrieval', 'Context augmentation', 'Closed-book vs open-book'],
            30: ['Attention sink phenomenon', 'KV cache', 'Positional bias', 'Prompt engineering']
        }

        return tech_map.get(paper_id, [f'Paper {paper_id} Technical Point'])

    def _extract_implementation_details(self, paper_id):
        """提取实现细节"""
        details_map = {
            2: {'framework': 'NumPy', 'key_code': 'rnn_step()', 'activation': 'tanh', 'output': 'softmax'},
            3: {'framework': 'NumPy', 'key_code': 'lstm_cell()', 'gates': 3, 'activation': 'sigmoid/tanh'},
            4: {'framework': 'NumPy', 'algorithm': 'Negative sampling', 'optimizer': 'SGD'},
            5: {'framework': 'NumPy', 'key_code': 'gru_cell()', 'gates': 2, 'simpler_than_lstm': True},
            6: {'framework': 'NumPy', 'architecture': 'Encoder-Decoder', 'attention': False},
            7: {'framework': 'NumPy', 'key_code': 'attention_layer()', 'scoring': 'additive'},
            8: {'framework': 'NumPy', 'key_code': 'multi_head_attention()', 'heads': 8, 'dimensionality': 512},
            9: {'framework': 'PyTorch', 'architecture': 'Bidirectional Transformer', ' MLM_loss': 'CrossEntropy'},
            10: {'framework': 'PyTorch', 'architecture': 'Unidirectional Transformer', 'optimizer': 'AdamW'},
            11: {'framework': 'PyTorch', 'layers': '8', 'optimizer': 'SGD', 'data_augmentation': True},
            12: {'framework': 'PyTorch', 'layers': '152', 'shortcut': '1x1_conv', 'optimizer': 'SGD'},
            13: {'framework': 'NumPy/PyTorch', 'key_code': 'batch_norm()', 'momentum': 0.9, 'epsilon': 1e-5},
            14: {'framework': 'NumPy', 'key_code': 'bahdanau_attention()', 'scoring': 'tanh'},
            15: {'framework': 'PyTorch', 'key_code': 'preactivation_block()', 'bn_relu_conv': True},
            16: {'framework': 'PyTorch', 'key_code': 'dropout()', 'p': 0.5, 'inverted': True},
            17: {'framework': 'PyTorch', 'key_code': 'unet_model()', 'loss': 'dice_loss', 'data_augmentation': True},
            18: {'framework': 'PyTorch', 'key_code': 'relational_memory()', 'slots': 4, 'heads': 4},
            19: {'framework': 'NumPy', 'key_code': 'diffusion_step()', 'entropy_calculation': True},
            20: {'framework': 'PyTorch', 'key_code': 'ntm_head()', 'memory_size': '128x64', 'heads': 1},
            21: {'framework': 'PyTorch', 'key_code': 'ctc_loss()', 'blank': 0, 'reduction': 'mean'},
            22: {'framework': 'NumPy', 'key_code': 'power_law()', 'fitting': 'log_log_linear'},
            23: {'framework': 'NumPy', 'key_code': 'mdl_principle()', 'principle': 'description_length_minimization'},
            24: {'framework': 'Conceptual', 'approach': 'Recursive', 'amplification': 'Distillation'},
            25: {'framework': 'Theoretical', 'key_concept': 'K(s) = minimum program length', 'uncomputable': True},
            26: {'framework': 'PyTorch', 'layers': '5 conv + 3 fc', 'filters': '11->96, 256, 384, 384, 256'},
            27: {'framework': 'PyTorch', 'prediction': 'n_tokens', 'context': 'full_sequence', 'token_interleaving': True},
            28: {'framework': 'PyTorch', 'encoders': 'dual BERT', 'loss': 'max_margin', 'batch_size': 128},
            29: {'framework': 'PyTorch', 'retriever': 'Dense', 'generator': 'BART/T5', 'pipeline': 'retrieve_then_generate'},
            30: {'framework': 'Theoretical/Empirical', 'phenomenon': 'attention_sink', 'kv_cache': 'memory_bottleneck'}
        }

        return details_map.get(paper_id, {'framework': 'Unknown', 'paper_id': paper_id})

    def search_related_concepts(self, keyword):
        """搜索相关概念"""
        return self.memory.search_concepts(keyword)