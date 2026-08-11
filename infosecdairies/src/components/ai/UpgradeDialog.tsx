/**
 * UpgradeDialog — freemium upsell dialog.
 * Shown either when a free user/guest hits the daily message limit (429) or on
 * the /chat premium gate.
 *
 * CTA differs by auth state:
 *  - Guest (not logged in): "Login / Create account" (→ /auth) is the primary
 *    action — they must log in and join a course for full access.
 *  - Signed-in free user: "Browse Courses" (→ /courses) is the primary action.
 */

import React from "react";
import { useNavigate } from "react-router-dom";
import { Crown, Sparkles } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { useAiAssistant } from "@/context/AiAssistantContext";
import { useAuth } from "@/context/AuthContext";

export interface UpgradeDialogProps {
  variant: "limit" | "gate";
}

export const UpgradeDialog: React.FC<UpgradeDialogProps> = ({ variant }) => {
  const { upgradeOpen, closeUpgrade } = useAiAssistant();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const isGuest = !isAuthenticated;
  const isLimit = variant === "limit";
  const title = isLimit
    ? "You've reached today's free limit"
    : "The AI Workspace is a premium feature";
  const description = isGuest
    ? isLimit
      ? "Free users get 5 AI messages per day. Login and join a BlueTeamers course to unlock unlimited AI messages and the full AI Workspace."
      : "Login and join a BlueTeamers course to unlock the full AI Workspace with unlimited conversations, page-aware assistance, and advanced practice labs."
    : isLimit
    ? "Free users get 5 AI messages per day. Join a BlueTeamers course to unlock unlimited AI messages and the full AI Workspace."
    : "Join a BlueTeamers course to unlock the full AI Workspace with unlimited conversations, page-aware assistance, and advanced practice labs.";

  return (
    <Dialog open={upgradeOpen} onOpenChange={closeUpgrade}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <div className="mb-2 inline-flex h-12 w-12 items-center justify-center rounded-2xl border border-primary/30 bg-primary/10">
            <Crown className="h-6 w-6 text-primary" />
          </div>
          <DialogTitle className="text-lg">{title}</DialogTitle>
          <DialogDescription className="text-sm leading-relaxed">
            {description}
          </DialogDescription>
        </DialogHeader>

        <div className="flex items-center gap-3 rounded-xl border border-primary/20 bg-primary/5 p-3 text-sm">
          <Sparkles className="h-4 w-4 shrink-0 text-primary" />
          <span>
            Get <span className="font-semibold text-foreground">full access</span> — unlimited AI
            answers with page context on every course, lesson and lab.
          </span>
        </div>

        <DialogFooter className="sm:justify-between">
          {isGuest ? (
            <>
              <Button variant="ghost" onClick={() => navigate("/courses")}>
                Browse Courses
              </Button>
              <Button
                onClick={() => {
                  closeUpgrade();
                  navigate("/auth");
                }}
                className="gap-2"
              >
                <Crown className="h-4 w-4" />
                Login / Create account
              </Button>
            </>
          ) : (
            <>
              <Button variant="ghost" onClick={closeUpgrade}>
                Maybe Later
              </Button>
              <Button
                onClick={() => {
                  closeUpgrade();
                  navigate("/courses");
                }}
                className="gap-2"
              >
                <Crown className="h-4 w-4" />
                Browse Courses
              </Button>
            </>
          )}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
