import { Settings, User, PenLine, MessageSquare } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

interface SidebarProps {
  currentView: string;
  onNavigate: (view: string) => void;
  userId: string;
  onUserIdChange: (id: string) => void;
}

export function Sidebar({ currentView, onNavigate, userId, onUserIdChange }: SidebarProps) {
  return (
    <div className="w-64 border-r bg-muted/40 min-h-screen p-4 flex flex-col">
      <div className="mb-8 px-4 py-2 flex items-center gap-3">
        <img src="/logo.png" alt="Mem U Trader Logo" className="h-8 w-8 object-contain" />
        <h1 className="text-xl font-bold">Mem U Trader</h1>
      </div>
      
      <div className="px-4 mb-6">
        <label htmlFor="user-id" className="text-xs font-medium text-muted-foreground mb-1.5 block">
          User ID
        </label>
        <Input
          id="user-id"
          value={userId}
          onChange={(e) => onUserIdChange(e.target.value)}
          placeholder="Enter User ID"
          className="h-8 text-sm"
        />
      </div>

      <nav className="space-y-2 flex-1">
        <Button 
          variant={currentView === 'input-memory' ? "secondary" : "ghost"} 
          className="w-full justify-start gap-2"
          onClick={() => onNavigate('input-memory')}
        >
          <PenLine className="h-4 w-4" />
          Input memory
        </Button>
        <Button 
          variant={currentView === 'ask-ai' ? "secondary" : "ghost"} 
          className="w-full justify-start gap-2"
          onClick={() => onNavigate('ask-ai')}
        >
          <MessageSquare className="h-4 w-4" />
          Ask to AI
        </Button>
        <Button 
          variant={currentView === 'profile' ? "secondary" : "ghost"} 
          className="w-full justify-start gap-2"
          onClick={() => onNavigate('profile')}
        >
          <User className="h-4 w-4" />
          Profile
        </Button>
        <Button 
          variant={currentView === 'settings' ? "secondary" : "ghost"} 
          className="w-full justify-start gap-2"
          onClick={() => onNavigate('settings')}
        >
          <Settings className="h-4 w-4" />
          Settings
        </Button>
      </nav>
      <div className="p-4 border-t">
        <p className="text-sm text-muted-foreground">© 2026 MemU Inc.</p>
      </div>
    </div>
  )
}
