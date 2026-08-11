import { Lock } from "lucide-react";
import labsPreview from "@/assets/labs-preview.png";

interface LabsComingSoonProps {
  activeItem: string;
}

const LabsComingSoon = ({ activeItem }: LabsComingSoonProps) => {
  return (
    <div className="fixed inset-0 z-0">
      {/* Full-page blurred dashboard background */}
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: `url(${labsPreview})` }}
      />

      {/* Dark blur overlay — full page */}
      <div className="absolute inset-0 backdrop-blur-sm bg-black/60" />

      {/* Centered access-denied card */}
      <div className="absolute inset-0 flex items-center justify-center px-4">
        <div className="text-center max-w-sm w-full">
          <div className="w-16 h-16 rounded-full bg-white/10 border border-white/20 flex items-center justify-center mx-auto mb-5 shadow-lg shadow-black/40">
            <Lock className="w-8 h-8 text-white" />
          </div>
          <h2 className="text-xl md:text-2xl font-semibold text-white mb-2">
            You don't have access to this page
          </h2>
          <p className="text-sm text-white/60 leading-relaxed">
            Please upgrade your plan or contact the administrator
          </p>
        </div>
      </div>
    </div>
  );
};

export default LabsComingSoon;
