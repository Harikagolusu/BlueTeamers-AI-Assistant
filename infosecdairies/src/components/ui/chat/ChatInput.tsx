import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Image as ImageIcon, Terminal, X, Paperclip } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { LanguageSelector } from './LanguageSelector';

interface ChatInputProps {
  onSendMessage: (text: string, attachments?: Array<{ name: string; type: string; content: string }>) => void;
  onStop: () => void;
  isLoading: boolean;
  language?: string;
  onLanguageChange?: (code: string) => void;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, onStop, isLoading, language, onLanguageChange }) => {
  const [input, setInput] = useState('');
  const [attachments, setAttachments] = useState<Array<{ name: string; type: string; content: string }>>([]);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [input]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;
    const filesArray = Array.from(e.target.files);

    filesArray.forEach((file) => {
      const reader = new FileReader();
      reader.onload = (event) => {
        if (event.target?.result) {
          setAttachments((prev) => [
            ...prev,
            {
              name: file.name,
              type: file.type,
              content: event.target.result as string,
            },
          ]);
        }
      };

      // PDFs and images are read as base64 data URLs so the backend can decode
      // them (PDF text is extracted server-side). Text/log files are read as
      // plain text so their content is directly analyzable.
      if (/\.pdf$/i.test(file.name) || file.type.startsWith('image/')) {
        reader.readAsDataURL(file);
      } else {
        reader.readAsText(file);
      }
    });

    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const removeAttachment = (index: number) => {
    setAttachments((prev) => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = () => {
    if ((!input.trim() && attachments.length === 0) || isLoading) return;
    onSendMessage(input, attachments);
    setInput('');
    setAttachments([]);
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const triggerFileSelect = () => {
    if (fileInputRef.current) fileInputRef.current.click();
  };

  return (
    <div className="flex flex-col w-full bg-zinc-950/80 backdrop-blur-xl border border-primary/20 rounded-2xl p-3 shadow-2xl relative">
      {/* Attachments Preview */}
      {attachments.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-3 px-1">
          {attachments.map((att, attIdx) => (
            <div key={attIdx} className="relative flex items-center gap-2 p-1.5 pr-8 rounded-lg bg-zinc-900 border border-primary/30 text-xs">
              {att.type.startsWith('image/') ? (
                <img src={att.content} alt={att.name} className="w-10 h-10 rounded object-cover" />
              ) : (
                <div className="w-10 h-10 rounded bg-muted flex items-center justify-center">
                  <Terminal className="w-5 h-5 text-primary" />
                </div>
              )}
              <div className="flex flex-col">
                <span className="max-w-[120px] truncate font-medium text-foreground">{att.name}</span>
                <span className="text-[10px] text-muted-foreground uppercase">{att.type.split('/')[1] || 'FILE'}</span>
              </div>
              <button 
                type="button" 
                onClick={() => removeAttachment(attIdx)}
                className="absolute right-1.5 top-1.5 p-1 rounded-full bg-zinc-800 hover:bg-destructive/80 text-muted-foreground hover:text-white transition-all"
              >
                <X className="w-3 h-3" />
              </button>
            </div>
          ))}
        </div>
      )}

      <div className="flex items-end gap-2">
        <input 
          type="file" 
          ref={fileInputRef}
          onChange={handleFileChange}
          multiple
          accept=".txt,.log,.csv,.json,.xml,.md,.pdf,text/plain"
          className="hidden"
        />
        
        <button
          type="button"
          onClick={triggerFileSelect}
          className="p-2.5 rounded-xl text-muted-foreground hover:text-primary hover:bg-primary/10 transition-colors"
          title="Attach files or images"
        >
          <Paperclip className="w-5 h-5" />
        </button>

        {onLanguageChange && (
          <LanguageSelector
            value={language || 'auto'}
            onChange={onLanguageChange}
            className="shrink-0"
          />
        )}

        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Message BlueTeamers AI..."
          className="bt-mono flex-1 max-h-[200px] min-h-[44px] bg-transparent border-0 resize-none focus:outline-none focus:ring-0 text-sm leading-relaxed p-2.5 text-foreground placeholder:text-muted-foreground scrollbar-thin scrollbar-thumb-zinc-700"
          rows={1}
          disabled={isLoading}
        />

        {isLoading ? (
          <Button
            type="button"
            variant="destructive"
            size="icon"
            onClick={onStop}
            className="h-10 w-10 shrink-0 rounded-xl transition-all"
            title="Stop generation"
          >
            <Loader2 className="w-5 h-5 animate-spin" />
          </Button>
        ) : (
          <Button 
            type="button" 
            onClick={handleSubmit}
            disabled={!input.trim() && attachments.length === 0}
            className="h-10 w-10 shrink-0 rounded-xl bg-primary hover:bg-primary/90 text-primary-foreground shadow-[0_0_10px_rgba(0,186,216,0.3)] disabled:bg-muted disabled:shadow-none transition-all"
          >
            <Send className="w-4 h-4 ml-0.5" />
          </Button>
        )}
      </div>
    </div>
  );
};
