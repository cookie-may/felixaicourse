// AI Glossary - What people say vs what things actually mean
// Source: https://github.com/rohitg00/ai-engineering-from-scratch

export interface GlossaryEntry {
  term: string;
  says: string;
  means: string;
}

export const GLOSSARY: GlossaryEntry[] = [
  {
    term: "Agent",
    says: "An autonomous AI that thinks and acts on its own",
    means: "A while loop where an LLM decides what tool to call next, executes it, sees the result, and repeats"
  },
  {
    term: "Attention",
    says: "How the AI focuses on important parts",
    means: "A mechanism where every token computes a weighted sum of all other tokens' values, with weights determined by how relevant they are (via dot product of query and key vectors)"
  },
  {
    term: "Alignment",
    says: "Making AI safe",
    means: "The technical challenge of making an AI system's behavior match human intentions, values, and preferences, including edge cases the designer didn't anticipate"
  },
  {
    term: "Autoregressive",
    says: "The AI generates one word at a time",
    means: "A model that predicts the next token conditioned on all previous tokens, then feeds that prediction back as input for the next step. GPT, LLaMA, and Claude are all autoregressive."
  },
  {
    term: "Activation Function",
    says: "The nonlinear thing between layers",
    means: "A function applied after each linear layer that introduces nonlinearity. Without it, stacking any number of linear layers collapses to a single linear transformation. ReLU, GELU, and SiLU are the most common. The choice directly affects whether gradients flow during training."
  },
  {
    term: "Adam (Optimizer)",
    says: "The default optimizer",
    means: "Adaptive Moment Estimation. Combines momentum (first moment) with adaptive learning rates per parameter (second moment). Has bias correction for early steps. Works well across most tasks without much tuning."
  },
  {
    term: "AdamW",
    says: "Adam but better",
    means: "Adam with decoupled weight decay. In standard Adam, L2 regularization gets scaled by the adaptive learning rate per parameter, which is not what you want. AdamW applies weight decay directly to the weights, independent of the gradient statistics. The default optimizer for training transformers."
  },
  {
    term: "Autograd",
    says: "Automatic gradients",
    means: "A system that records operations on tensors and automatically computes gradients via reverse-mode differentiation. PyTorch's autograd builds a computation graph on-the-fly (dynamic graph), while JAX uses function transformations (grad). This is what makes backpropagation practical -- you write the forward pass, and the framework computes all the derivatives."
  },
  {
    term: "Batch Size",
    says: "How many examples at once",
    means: "The number of training examples processed in one forward/backward pass before updating weights. Larger batches give more stable gradient estimates but use more memory. Typical values: 32-512 for training, larger for inference. Batch size interacts with learning rate -- double the batch, double the LR (linear scaling rule)."
  },
  {
    term: "Backpropagation",
    says: "How neural networks learn",
    means: "An algorithm that computes how much each weight contributed to the error by applying the chain rule backward through the network, then adjusts weights proportionally"
  },
  {
    term: "Context Window",
    says: "How much the AI can remember",
    means: "The maximum number of tokens (input + output) that fit in a single API call. Not memory — it's a fixed-size buffer that resets every call"
  },
  {
    term: "Chain of Thought (CoT)",
    says: "Making the AI think step by step",
    means: "A prompting technique where you ask the model to show its reasoning steps, which improves accuracy on multi-step problems because each step conditions the next token generation"
  },
  {
    term: "CNN (Convolutional Neural Network)",
    says: "Image AI",
    means: "A neural network that uses convolution operations (sliding filters over the input) to detect local patterns. Stacking convolutions detects increasingly complex features: edges, textures, objects."
  },
  {
    term: "CUDA",
    says: "GPU programming",
    means: "NVIDIA's parallel computing platform. Lets you run matrix operations on thousands of GPU cores simultaneously. PyTorch and TensorFlow use CUDA under the hood."
  },
  {
    term: "Chunking",
    says: "Splitting documents into pieces",
    means: "Breaking long text into smaller segments for retrieval. Choices include: character count (simple but ignores semantic boundaries), sentence-based (better semantic coherence), or semantic chunking (clusters similar sentences). Chunks are embedded and stored in a vector database. Chunk size and overlap directly affect retrieval quality."
  },
  {
    term: "Constitutional AI",
    says: "AI that follows rules",
    means: "A technique where you give the model a set of principles (the 'constitution') and have it critique and revise its own outputs based on these principles. Anthropic introduced this for Claude, using RLHF-like feedback without human labeling of every instance."
  },
  {
    term: "Context Engineering",
    says: "Putting stuff in the prompt",
    means: "The discipline of structuring, ordering, and optimizing all the information passed to an LLM in a single call. Includes: instruction placement (system prompt first), few-shot examples, retrieved context windows, chain of thought, and output format constraints. Small changes in ordering can dramatically change results."
  },
  {
    term: "Contrastive Learning",
    says: "Learning by comparing",
    means: "A self-supervised technique where the model learns representations by pulling similar examples together and pushing dissimilar ones apart. SimCLR, CLIP, and sentence transformers use this. Works by creating augmentations of the same image/text and training the model to recognize they're similar."
  },
  {
    term: "Convolution",
    says: "A sliding window thing",
    means: "An operation where a small filter (kernel) slides across the input, computing a weighted sum at each position. Detects features like edges in images or patterns in time series. The weights are learned during training. Padding and stride control output size."
  },
  {
    term: "Cross-Entropy Loss",
    says: "The default loss function",
    means: "Measures the difference between the predicted probability distribution and the true distribution. For classification, it's the negative log likelihood of the correct class. Minimizing cross-entropy is equivalent to maximum likelihood estimation. Widely used because it has nice gradients and works well with softmax."
  },
  {
    term: "Decoder",
    says: "The part that generates output",
    means: "The component that produces tokens one at a time, conditioned on all previous tokens (autoregressive). In transformers, the decoder has masked self-attention (can't see future tokens) and cross-attention to encoder outputs. GPT is a decoder-only model."
  },
  {
    term: "Dimensionality Reduction",
    says: "Making things smaller",
    means: "Techniques to represent high-dimensional data in fewer dimensions while preserving important structure. PCA finds linear projections with maximum variance. t-SNE and UMAP are nonlinear and better at preserving local structure for visualization."
  },
  {
    term: "Distributed Training",
    says: "Training on multiple GPUs",
    means: "Techniques to parallelize training across multiple GPUs/machines. Data parallelism splits batches across GPUs. Model parallelism splits the model itself. FSDP (Fully Sharded Data Parallel) shards model weights. Synchronous vs asynchronous updates. Communication bandwidth is often the bottleneck."
  },
  {
    term: "DPO (Direct Preference Optimization)",
    says: "Better than PPO for alignment",
    means: "A simplification of RLHF that formulates preference learning as a binary classification problem. Uses a reference model to compute which response is preferred, without the complexity of training a separate reward model. Simpler implementation, faster training, often comparable results to RLHF."
  },
  {
    term: "Embedding",
    says: "Converting text to numbers",
    means: "A learned vector representation of tokens, sentences, or documents that captures semantic meaning. Trained by predicting neighboring context (word2vec) or through contrastive learning (CLIP). Enables math on text: similar meanings = similar vectors. Stored in vector databases for RAG."
  },
  {
    term: "Encoder",
    says: "The part that reads input",
    means: "The component that processes the full input sequence simultaneously (bidirectional). In transformers, the encoder has self-attention without masking. Produces representations used by decoder for generation. BERT is encoder-only."
  },
  {
    term: "Fine-tuning",
    says: "Training on your data",
    means: "Continuing training of a pre-trained model on a specific task or domain. Full fine-tuning updates all parameters. Parameter-efficient methods (LoRA, adapters) update only a small subset, reducing memory and catastrophic forgetting. Task-specific data usually improves performance over base models."
  },
  {
    term: "Flash Attention",
    says: "Fast attention",
    means: "An attention implementation that uses tiling to compute attention without materializing the full attention matrix. Reduces memory from O(n²) to O(n) and speeds up training 2-4x. Exploits GPU memory hierarchy. Now standard in modern LLM training."
  },
  {
    term: "GAN (Generative Adversarial Network)",
    says: "Two AIs fighting",
    means: "A generator creates samples; a discriminator tries to distinguish real from fake. They train jointly in a minimax game. Generator improves until discriminator can't tell the difference. Famous for images (StyleGAN, BigGAN) but training is unstable and mode collapse is a common problem."
  },
  {
    term: "GELU (Gaussian Error Linear Unit)",
    says: "The fancy activation",
    means: "Gaussian Error Linear Unit. Approximates x * sigmoid(1.702x) but is actually x * Φ(x) where Φ is the Gaussian CDF. More expensive than ReLU but smoother gradients. The default activation in modern transformers (BERT, GPT, ViT)."
  },
  {
    term: "Gradient Clipping",
    says: "Preventing exploding gradients",
    means: "Scaling gradients when their norm exceeds a threshold (typically 1.0). Prevents gradient explosion during training, especially in RNNs and early transformer训练. Doesn't solve the underlying problem but is a simple safeguard."
  },
  {
    term: "Gradient Descent",
    says: "Following the slope downhill",
    means: "An optimization algorithm that updates parameters in the direction of steepest descent of the loss function. The learning rate determines step size. Variants include SGD (stochastic, uses batches), Adam (adaptive rates), and RMSprop (per-parameter learning rates)."
  },
  {
    term: "Hallucination",
    says: "When AI makes stuff up",
    means: "Confident generation of factually incorrect or nonsensical content. Root causes: training on flawed data, memorization rather than reasoning, lack of grounding in facts, and maximization of fluency over accuracy. Mitigations: retrieval augmentation, chain of thought, uncertainty quantification, and human feedback."
  },
  {
    term: "Hyperparameter",
    says: "Settings to tune",
    means: "Parameters set before training that control the learning process. Examples: learning rate, batch size, number of layers, attention heads, dropout rate. Unlike model weights, hyperparameters aren't learned from data. Tuned via grid search, random search, or Bayesian optimization."
  },
  {
    term: "Inference",
    says: "Running the model",
    means: "Using a trained model to make predictions on new data. Contrast with training. For LLMs, inference is often the expensive part in production — models are large and generation is slow. Optimization techniques: quantization, batching, KV caching, speculative decoding."
  },
  {
    term: "KV Cache",
    says: "Caching for faster generation",
    means: "Storing key and value matrices from attention computations so they don't need to be recomputed for each new token. Critical for efficient autoregressive generation. Memory grows linearly with sequence length and batch size. Flash attention makes KV cache management more efficient."
  },
  {
    term: "Layer Normalization",
    says: "Normalizing each layer",
    means: "Normalizes activations across features (channels) within a single example. Computes mean and variance across the feature dimension, then rescales with learned gamma/beta. Applied before each sub-layer in transformers. Stabilizes training and enables deeper networks."
  },
  {
    term: "Learning Rate",
    says: "How fast it learns",
    means: "The step size multiplier in gradient descent. Too high: training diverges. Too low: training is slow and may get stuck. Often uses schedules: warmup (gradually increase), decay (reduce over time), or cyclical. Adam adapts learning rates per parameter automatically."
  },
  {
    term: "LLaMA",
    says: "Meta's open model",
    means: "A family of open-source language models by Meta. Ranges from 7B to 70B parameters. Uses transformer architecture with improvements (RMSNorm, SwiGLU, RoPE). The 13B model is competitive with GPT-3 (175B) due to efficiency. Many fine-tuned variants exist."
  },
  {
    term: "LoRA (Low-Rank Adaptation)",
    says: "Efficient fine-tuning",
    means: "Adds small trainable rank-decomposition matrices alongside frozen pretrained weights. Reduces trainable parameters by 1000x with minimal performance loss. Different adapters can be swapped for different tasks. The go-to method for parameter-efficient fine-tuning."
  },
  {
    term: "Loss Function",
    says: "How we measure error",
    means: "A function that quantifies how wrong a model's predictions are. The training objective is to minimize this. Cross-entropy for classification, MSE for regression. The choice affects what the model learns and the geometry of the optimization landscape."
  },
  {
    term: "Masked Language Modeling",
    says: "Fill in the blank",
    means: "A pretraining objective where random tokens are replaced with a [MASK] token and the model must predict the original token. Used by BERT. Doesn't teach the model to generate — only to understand context. Creates unidirectional representations."
  },
  {
    term: "Maximum Likelihood Estimation",
    says: "Finding the most likely parameters",
    means: "A statistical method that finds parameters that maximize the probability of observing the training data. Equivalent to minimizing cross-entropy loss. The foundation of most neural network training."
  },
  {
    term: "Mixture of Experts (MoE)",
    says: "Different parts for different inputs",
    means: "A model architecture where different 'expert' networks handle different types of inputs. A routing mechanism selects which experts to activate for each input. Allows massive models with constant compute cost per token. Switch Transformer, Mixtral, and GPT-4 are rumored to use MoE."
  },
  {
    term: "Model Distillation",
    says: "Small model learns from big model",
    means: "Training a smaller model to mimic a larger model's outputs or internal representations. Uses soft targets (probability distributions) from the teacher instead of hard labels. Can compress knowledge 10-100x while retaining most performance."
  },
  {
    term: "Multimodal",
    says: "AI that sees and hears",
    means: "Models that process multiple types of data: text, images, audio, video. Requires aligned representations across modalities. CLIP aligned images and text. GPT-4V processes images. Audio-Visual models exist. True any-to-any generation is an active research area."
  },
  {
    term: "Neural Network",
    says: "AI brain",
    means: "A differentiable function that learns to map inputs to outputs via gradient descent. Composed of layers of simple functions (linear transformation + nonlinear activation). 'Hidden layers' learn intermediate representations. Depth (layers) enables hierarchical feature learning."
  },
  {
    term: "One-Shot Learning",
    says: "Learning from one example",
    means: "A model must learn to recognize a category after seeing only a single example. Contrast with few-shot (few examples) and zero-shot (no examples, uses transferred knowledge). Metric learning approaches (Siamese networks) are common."
  },
  {
    term: "Overfitting",
    says: "Memorizing instead of learning",
    means: "When a model learns the training data too well, including noise and irrelevant patterns, and performs poorly on new data. The model has high variance. Mitigations: regularization, dropout, early stopping, data augmentation, cross-validation."
  },
  {
    term: "Perceptron",
    says: "The simplest neural network",
    means: "A single neuron that computes a weighted sum of inputs and applies a step function. The original neural network (1957). Can't learn XOR — the motivation for multilayer networks. Foundation for understanding modern deep learning."
  },
  {
    term: "Positional Encoding",
    says: "Where words are",
    means: "A mechanism to inject position information into transformers, which have no inherent notion of order. Options: sinusoidal (fixed patterns), learned (trainable), RoPE (rotary, relative positions), ALiBi (attention with linear biases). Critical for sequence modeling."
  },
  {
    term: "Prompt Engineering",
    says: "Writing instructions for AI",
    means: "Crafting inputs to get desired outputs from LLMs. Techniques include: clear task description, few-shot examples, chain of thought, output format constraints, and system prompts. More art than science but patterns exist."
  },
  {
    term: "Quantization",
    says: "Making models smaller",
    means: "Reducing weight precision (e.g., 32-bit float → 8-bit int) to decrease model size and speed up inference. Post-training quantization is simple but loses accuracy. Quantization-aware training preserves more performance. GPTQ, AWQ, and GGUF are popular methods."
  },
  {
    term: "RAG (Retrieval-Augmented Generation)",
    says: "AI that can look things up",
    means: "A pattern where an LLM retrieves relevant documents from a knowledge base and includes them in the context for generation. Reduces hallucination, enables up-to-date knowledge, and allows grounding in specific documents. Components: embedding model, vector database, retriever, generator."
  },
  {
    term: "ReLU (Rectified Linear Unit)",
    says: "The simple activation",
    means: "f(x) = max(0, x). Simple and effective. Sparse activation (only active for positive inputs). Solves vanishing gradient problem in shallow networks. Variants: Leaky ReLU (small slope for negatives), PReLU (learned slope). Still common but GELU is preferred for transformers."
  },
  {
    term: "RLHF (Reinforcement Learning from Human Feedback)",
    says: "Training AI with human preferences",
    means: "A three-stage process: supervised fine-tuning, reward model training (humans rank outputs), and policy optimization (PPO against reward model). Makes models like ChatGPT helpful, harmless, and honest. Expensive due to human labeling. DPO is a simpler alternative."
  },
  {
    term: "RoPE (Rotary Position Embedding)",
    says: "Better position encoding",
    means: "Encodes position by rotating the key and query vectors in attention. Naturally captures relative positions without needing separate positional bias. Used by LLaMA, PaLM, and others. Better extrapolation to longer sequences than learned or sinusoidal encodings."
  },
  {
    term: "Sampling",
    says: "Picking the next word",
    means: "The process of selecting the next token from the model's probability distribution. Greedy (always pick most likely) is deterministic but repetitive. Temperature scaling adjusts distribution sharpness. Top-k and top-p (nucleus) sampling introduce controlled randomness for diversity."
  },
  {
    term: "Self-Attention",
    says: "Words looking at other words",
    means: "A mechanism where each position attends to all positions in the sequence, computing weights based on learned query, key, and value projections. Captures long-range dependencies without recurrence. The core of transformer architectures."
  },
  {
    term: "SFT (Supervised Fine-Tuning)",
    says: "Fine-tuning with examples",
    means: "Fine-tuning a pretrained model on demonstrations of desired behavior. Uses human-written or AI-generated (with good prompts) input-output pairs. The first stage of RLHF. Much simpler than reinforcement learning but requires high-quality data."
  },
  {
    term: "Softmax",
    says: "Making probabilities",
    means: "A function that converts a vector of real numbers into a probability distribution (all outputs sum to 1, all positive). Used at the output of classification models. Temperature-adjusted softmax controls how 'peaked' the distribution is."
  },
  {
    term: "Token",
    says: "A piece of a word",
    means: "The unit of text that models process. Not characters or words — a learned subword unit. GPT-4 uses ~10-15 chars per token on average (larger vocab than GPT-3.5's ~4 chars). Models have context windows measured in tokens, not words."
  },
  {
    term: "Tokenizer",
    says: "Breaking text into pieces",
    means: "The algorithm that converts text to tokens. Common approaches: BPE (Byte Pair Encoding, used by GPT), WordPiece (used by BERT), SentencePiece (language-agnostic). Training learns frequent subword units from corpus. Tokenizer choice affects vocabulary size and out-of-vocabulary handling."
  },
  {
    term: "Transformer",
    says: "The architecture that changed everything",
    means: "A neural network architecture using self-attention and feedforward layers. No recurrence — processes entire sequence in parallel. Introduced in 'Attention Is All You Need' (2017). Scales better than RNNs. Foundation of modern LLMs, vision transformers, and more."
  },
  {
    term: "Underfitting",
    says: "Not learning enough",
    means: "When a model fails to capture the underlying pattern in the data. The model has high bias. Symptoms: poor training and validation performance. Fixes: larger model, more features, longer training, less regularization."
  },
  {
    term: "Vector Database",
    says: "Database for embeddings",
    means: "A database optimized for storing and searching high-dimensional vectors. Enables nearest neighbor search by semantic similarity. Popular: Pinecone, Weaviate, Chroma, Qdrant. Critical for RAG. Indexes like HNSW enable fast approximate nearest neighbor search."
  },
  {
    term: "Vision Transformer (ViT)",
    says: "Transformers for images",
    means: "Treats images as sequences of patches (16x16 pixels each), linearly embedded, then processed by transformer encoder. No convolutions. Benefits: learns global dependencies, scales well with data. Outperforms CNNs on large datasets. The foundation for many vision models."
  },
  {
    term: "Weight Decay",
    says: "Regularization for weights",
    means: "An L2 regularization penalty on model weights. Prevents weights from growing too large, providing implicit regularization. The strength (coefficient) is a hyperparameter. Often decoupled from learning rate in AdamW for better regularization behavior."
  },
  {
    term: "Zero-Shot Learning",
    says: "AI that never saw your task",
    means: "A model performs a task without any task-specific training examples. Uses knowledge transferred from pretraining. The model reasons about the task description given in the input. GPT-3 showed that large language models exhibit impressive zero-shot capabilities."
  }
];

export function searchGlossary(query: string): GlossaryEntry[] {
  const lowerQuery = query.toLowerCase();
  return GLOSSARY.filter(entry =>
    entry.term.toLowerCase().includes(lowerQuery) ||
    entry.says.toLowerCase().includes(lowerQuery) ||
    entry.means.toLowerCase().includes(lowerQuery)
  );
}
