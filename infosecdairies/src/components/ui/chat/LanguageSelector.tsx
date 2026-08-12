import React from 'react';
import { Languages } from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { cn } from '@/lib/utils';

export interface LanguageOption {
  code: string;
  label: string;
}

// Mirrors the backend language catalog (app/multilingual/languages.py).
const LANGUAGE_OPTIONS: LanguageOption[] = [
  { code: 'auto', label: 'Auto Detect' },
  { code: 'en', label: 'English' },
  { code: 'te', label: 'Telugu (తెలుగు)' },
  { code: 'te+en', label: 'Tinglish (తెలుగు + English)' },
  { code: 'hi', label: 'Hindi (हिन्दी)' },
  { code: 'hi+en', label: 'Hinglish (हिन्दी + English)' },
  { code: 'ta', label: 'Tamil (தமிழ்)' },
  { code: 'ta+en', label: 'Tanglish (தமிழ் + English)' },
  { code: 'kn', label: 'Kannada (ಕನ್ನಡ)' },
  { code: 'kn+en', label: 'Kanglish (ಕನ್ನಡ + English)' },
  { code: 'ml', label: 'Malayalam (മലയാളം)' },
  { code: 'ml+en', label: 'Manglish (മലയാളം + English)' },
  { code: 'bn', label: 'Bengali (বাংলা)' },
  { code: 'bn+en', label: 'Banglish (বাংলা + English)' },
  { code: 'mr', label: 'Marathi (मराठी)' },
  { code: 'mr+en', label: 'Marathish (मराठी + English)' },
  { code: 'gu', label: 'Gujarati (ગુજરાતી)' },
  { code: 'gu+en', label: 'Gujarlish (ગુજરાતી + English)' },
  { code: 'pa', label: 'Punjabi (ਪੰਜਾਬੀ)' },
  { code: 'pa+en', label: 'Punglish (ਪੰਜਾਬੀ + English)' },
  { code: 'or', label: 'Odia (ଓଡ଼ିଆ)' },
  { code: 'or+en', label: 'Odia-English (ଓଡ଼ିଆ + English)' },
  { code: 'ur', label: 'Urdu (اردو)' },
  { code: 'ur+en', label: 'Urlish (اردو + English)' },
];

interface LanguageSelectorProps {
  value: string;
  onChange: (code: string) => void;
  className?: string;
}

export const LanguageSelector: React.FC<LanguageSelectorProps> = ({
  value,
  onChange,
  className,
}) => {
  const currentLabel =
    LANGUAGE_OPTIONS.find((opt) => opt.code === value)?.label ?? 'Auto Detect';

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button
          type="button"
          className={cn(
            'p-2 rounded-lg text-muted-foreground hover:text-primary hover:bg-primary/10 transition-colors',
            value !== 'auto' && 'text-primary',
            className,
          )}
          title={`Response language: ${currentLabel}`}
          aria-label={`Response language: ${currentLabel}`}
        >
          <Languages className="w-4 h-4" />
        </button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="start" className="max-h-80 overflow-y-auto w-56">
        <DropdownMenuRadioGroup value={value} onValueChange={onChange}>
          {LANGUAGE_OPTIONS.map((opt) => (
            <DropdownMenuRadioItem key={opt.code} value={opt.code}>
              {opt.label}
            </DropdownMenuRadioItem>
          ))}
        </DropdownMenuRadioGroup>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};
