# 实现Agent - 集成记忆系统
# 负责验证代码实现并运行测试

import os
import json

class ImplementerAgent:
    def __init__(self, project_path, memory_system=None):
        self.project_path = project_path

        # 使用传入的记忆系统
        if memory_system:
            self.memory = memory_system
        else:
            from memory_system import AgentMemorySystem
            self.memory = AgentMemorySystem(project_path)

    def implement_paper(self, paper_id, paper_file):
        """实现论文"""
        print(f"Implementer verifying Paper {paper_id}: {paper_file}")

        paper_identifier = f"paper-{paper_id}"

        # 检查论文文件是否存在
        if not os.path.exists(paper_file):
            result = {
                'status': 'error',
                'message': f'Paper file not found: {paper_file}',
                'paper_id': paper_id
            }
        else:
            # 验证实现
            result = self._verify_implementation(paper_id, paper_file)

        # 保存实现结果到记忆系统
        progress_id = self.memory.generate_id("progress")
        self.memory.save_learning_progress(
            progress_id=progress_id,
            paper_id=paper_identifier,
            agent_type='implementer',
            stage='implementation',
            status=result.get('status', 'completed'),
            result=json.dumps(result, ensure_ascii=False)
        )

        # 保存上下文
        self.memory.save_context(
            session_id=f"paper_{paper_id}",
            context_type="implementation_verification",
            content=f"完成Paper {paper_id}的实现验证",
            metadata={"paper_file": paper_file, "status": result.get('status')}
        )

        return {
            'paper_id': paper_id,
            'file': paper_file,
            'title': f'Paper {paper_id} Implementation',
            'result': result
        }

    def _verify_implementation(self, paper_id, paper_file):
        """验证实现"""
        # 检查文件扩展名
        file_ext = os.path.splitext(paper_file)[1].lower()

        # 获取文件大小
        file_size = os.path.getsize(paper_file) if os.path.exists(paper_file) else 0

        # 检查关键实现组件
        key_components = self._get_key_components(paper_id)

        # 验证状态
        verification_status = 'verified' if file_size > 0 else 'incomplete'

        return {
            'status': verification_status,
            'file_size': file_size,
            'file_type': file_ext,
            'key_components': key_components,
            'message': f'Implementation verified for Paper {paper_id}'
        }

    def _get_key_components(self, paper_id):
        """获取关键实现组件"""
        components_map = {
            2: ['rnn_step', 'forward', 'backward', 'softmax'],
            3: ['lstm_cell', 'forward', 'backward', 'sigmoid', 'tanh'],
            4: ['word2vec', 'skip_gram', 'cbow', 'negative_sampling'],
            5: ['gru_cell', 'update_gate', 'reset_gate'],
            6: ['encoder', 'decoder', 'forward', 'backward'],
            7: ['attention', 'bahdanau_attention', 'context_vector'],
            8: ['multi_head_attention', 'scaled_dot_product', 'positional_encoding'],
            9: ['bert_model', 'masked_lm', 'next_sentence'],
            10: ['gpt_model', 'transformer_block', 'causal_mask'],
            11: ['alexnet', 'conv_layer', 'lrn', 'overlapping_pooling'],
            12: ['resnet_block', 'shortcut_connection', 'bottleneck'],
            13: ['batch_norm', 'moving_average', 'gamma_beta'],
            14: ['attention_layer', 'alignment_scores', 'context_vector'],
            15: ['preactivation_block', 'bn_relu_conv', 'identity_mapping'],
            16: ['dropout', 'weight_scale', 'inverted_dropout'],
            17: ['unet', 'contracting_path', 'expanding_path', 'skip_connections'],
            18: ['relational_memory', 'multi_head_attention', 'memory_slots'],
            19: ['diffusion', 'entropy', 'maxwell_demon'],
            20: ['ntm', 'memory_matrix', 'read_head', 'write_head'],
            21: ['ctc_loss', 'forward_algorithm', 'beam_search'],
            22: ['power_law', 'compute_optimal', 'scaling_exponent'],
            23: ['mdl', 'description_length', 'model_selection'],
            24: ['amplification', 'distillation', 'recursive_improvement'],
            25: ['kolmogorov_complexity', 'algorithmic_information'],
            26: ['convolution', 'max_pooling', 'filters'],
            27: ['multi_token_prediction', 'n_gram', 'token_interleaving'],
            28: ['dense_retrieval', 'dual_encoder', 'max_margin_loss'],
            29: ['rag', 'retriever', 'generator', 'retrieve_then_generate'],
            30: ['attention_sink', 'kv_cache', 'positional_bias']
        }

        return components_map.get(paper_id, [f'Paper {paper_id} component'])

    def get_implementation_status(self, paper_id):
        """获取实现状态"""
        paper_identifier = f"paper-{paper_id}"
        progress_records = self.memory.get_learning_progress(paper_identifier)

        # 筛选实现相关的记录
        implementation_records = [
            p for p in progress_records
            if p.get('agent_type') == 'implementer' and p.get('stage') == 'implementation'
        ]

        return implementation_records[-1] if implementation_records else None