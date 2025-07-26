'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, Loader2, Trash2 } from 'lucide-react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function AIChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: "Hi! I'm your AI learning assistant. Ask me anything about AI engineering, machine learning, or concepts from the curriculum."
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [showKeyInput, setShowKeyInput] = useState(true);
  const [error, setError] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Check for stored API key
    const storedKey = localStorage.getItem('openrouter-api-key');
    if (storedKey) {
      setApiKey(storedKey);
      setShowKeyInput(false);
    }
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    if (!apiKey) {
      setError('Please enter your OpenRouter API key to use AI chat');
      return;
    }

    const userMessage: Message = { role: 'user', content: input.trim() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setError('');

    try {
      const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`,
          'HTTP-Referer': window.location.origin,
          'X-Title': 'SLAFAI',
        },
        body: JSON.stringify({
          model: 'anthropic/claude-3-haiku',
          messages: [
            {
              role: 'system',
              content: `You are an AI engineering tutor for the SLAFAI course.
              The course covers: Math foundations, ML fundamentals, Deep Learning, Computer Vision, NLP, Speech & Audio, Transformers, Generative AI, Reinforcement Learning, LLMs from Scratch, LLM Engineering, Multimodal AI, Tools & Protocols (MCP), Agent Engineering, Autonomous Systems, Multi-Agent & Swarms, Infrastructure & Production, Ethics & Safety.

              Provide clear, practical explanations. Use code examples when relevant. Don't be overly verbose. Be encouraging and supportive of learners.`
            },
            ...messages.map(m => ({ role: m.role, content: m.content })),
            { role: 'user', content: input.trim() }
          ],
          max_tokens: 1024,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error?.message || `API error: ${response.status}`);
      }

      const data = await response.json();
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.choices[0]?.message?.content || 'Sorry, I could not generate a response.'
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get response');
      // Remove the user message if the request failed
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
    }
  };

  const saveApiKey = (key: string) => {
    localStorage.setItem('openrouter-api-key', key);
    setApiKey(key);
    setShowKeyInput(false);
    setError('');
  };

  const clearChat = () => {
    setMessages([
      {
        role: 'assistant',
        content: "Hi! I'm your AI learning assistant. Ask me anything about AI engineering, machine learning, or concepts from the curriculum."
      }
    ]);
  };

  return (
    <div
      className="flex flex-col h-[600px] rounded-2xl border-2 overflow-hidden"
      style={{
        background: 'var(--bg-surface)',
        borderColor: 'var(--border)'
      }}
    >
      {/* Header */}
      <div
        className="p-4 border-b-2 flex justify-between items-center"
        style={{ borderColor: 'var(--border)' }}
      >
        <div className="flex items-center gap-3">
          <div
            className="w-10 h-10 rounded-full flex items-center justify-center"
            style={{ background: 'var(--accent)' }}
          >
            <Bot className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-heading text-lg">AI Tutor</h3>
            <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
              Powered by OpenRouter
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={clearChat}
            className="p-2 rounded-lg border transition-colors hover:border-[var(--accent)]"
            style={{ borderColor: 'var(--border)', color: 'var(--text-muted)' }}
            title="Clear chat"
          >
            <Trash2 className="w-4 h-4" />
          </button>
          <button
            onClick={() => {
              localStorage.removeItem('openrouter-api-key');
              setApiKey('');
              setShowKeyInput(true);
            }}
            className="px-3 py-1.5 rounded-lg border text-sm transition-colors hover:border-[var(--accent)]"
            style={{ borderColor: 'var(--border)', color: 'var(--text-muted)' }}
          >
            Change Key
          </button>
        </div>
      </div>

      {/* API Key Input */}
      {showKeyInput && (
        <div className="p-4 border-b-2" style={{ borderColor: 'var(--border)' }}>
          <p className="text-sm mb-3" style={{ color: 'var(--text-muted)' }}>
            Enter your OpenRouter API key to use AI chat:
          </p>
          <div className="flex gap-2">
            <input
              type="password"
              placeholder="sk-or-..."
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="flex-1 px-3 py-2 rounded-lg border-2 outline-none"
              style={{
                background: 'var(--bg)',
                borderColor: 'var(--border)',
                color: 'var(--text)'
              }}
            />
            <button
              onClick={() => saveApiKey(apiKey)}
              className="px-4 py-2 rounded-lg font-medium transition-colors"
              style={{
                background: 'var(--accent)',
                color: 'white'
              }}
            >
              Save
            </button>
          </div>
          <p className="text-xs mt-2" style={{ color: 'var(--text-muted)' }}>
            Get your key at{' '}
            <a
              href="https://openrouter.ai/keys"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: 'var(--secondary)' }}
            >
              openrouter.ai/keys
            </a>
          </p>
        </div>
      )}

      {/* Error */}
      {error && (
        <div
          className="p-3 mx-4 mt-4 rounded-lg text-sm"
          style={{
            background: 'rgba(239, 68, 68, 0.1)',
            color: '#ef4444',
            border: '1px solid rgba(239, 68, 68, 0.3)'
          }}
        >
          {error}
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
          >
            <div
              className="w-8 h-8 rounded-full flex items-center justify-center shrink-0"
              style={{
                background: msg.role === 'user' ? 'var(--secondary)' : 'var(--accent)'
              }}
            >
              {msg.role === 'user' ? (
                <User className="w-4 h-4 text-white" />
              ) : (
                <Bot className="w-4 h-4 text-white" />
              )}
            </div>
            <div
              className="max-w-[80%] px-4 py-3 rounded-2xl"
              style={{
                background: msg.role === 'user' ? 'var(--bg)' : 'var(--bg)',
                border: '1px solid var(--border)',
                color: 'var(--text)'
              }}
            >
              <p className="whitespace-pre-wrap text-sm leading-relaxed">
                {msg.content}
              </p>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex gap-3">
            <div
              className="w-8 h-8 rounded-full flex items-center justify-center"
              style={{ background: 'var(--accent)' }}
            >
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div
              className="px-4 py-3 rounded-2xl flex items-center gap-2"
              style={{
                background: 'var(--bg)',
                border: '1px solid var(--border)'
              }}
            >
              <Loader2 className="w-4 h-4 animate-spin" style={{ color: 'var(--accent)' }} />
              <span className="text-sm" style={{ color: 'var(--text-muted)' }}>
                Thinking...
              </span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form
        onSubmit={handleSubmit}
        className="p-4 border-t-2"
        style={{ borderColor: 'var(--border)' }}
      >
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={apiKey ? "Ask about AI engineering..." : "Enter API key above to chat"}
            disabled={!apiKey || isLoading}
            className="flex-1 px-4 py-3 rounded-xl border-2 outline-none"
            style={{
              background: 'var(--bg)',
              borderColor: 'var(--border)',
              color: 'var(--text)'
            }}
          />
          <button
            type="submit"
            disabled={!apiKey || isLoading || !input.trim()}
            className="px-4 py-3 rounded-xl transition-colors disabled:opacity-50"
            style={{
              background: 'var(--accent)',
              color: 'white'
            }}
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </form>
    </div>
  );
}
