import { useState } from "react"
import * as React from "react"
import { Sidebar } from "@/components/Sidebar"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { ThumbsUp, ThumbsDown } from "lucide-react"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

const CURRENCY_PAIRS = [
  "USD/JPY", "EUR/USD", "GBP/USD", "USD/CHF", "USD/CAD", 
  "AUD/USD", "NZD/USD", "EUR/JPY", "GBP/JPY", "CHF/JPY", 
  "CAD/JPY", "NZD/JPY", "ZAR/JPY", "MXN/JPY", "TRY/JPY", 
  "EUR/GBP", "EUR/AUD", "GBP/AUD", "AUD/NZD"
]

function App() {
  const [currentView, setCurrentView] = useState('input-memory')
  const [inputText, setInputText] = useState('')
  const [selectedCurrency, setSelectedCurrency] = useState('')
  const [isSending, setIsSending] = useState(false)
  const [userId, setUserId] = useState(() => localStorage.getItem('memu_user_id') || 'demo_user')

  React.useEffect(() => {
    localStorage.setItem('memu_user_id', userId)
  }, [userId])

  const handleSend = async () => {
    if (!inputText) {
      alert("Please input some information.")
      return
    }

    if (!userId.trim()) {
      alert("Please enter a User ID.")
      return
    }

    setIsSending(true)
    try {
      const response = await fetch('http://localhost:5001/memorize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          agent_id: selectedCurrency,
          user_message: inputText
        }),
      })

      if (response.ok) {
        alert("Memorized successfully!")
        setInputText("")
        setSelectedCurrency("")
      } else {
        const errorData = await response.json()
        alert(`Failed to memorize: ${errorData.error || response.statusText}`)
      }
    } catch (error) {
      console.error("Error calling memorize API:", error)
      alert("An error occurred while memorizing.")
    } finally {
      setIsSending(false)
    }
  }

  const [aiQuery, setAiQuery] = useState('')
  const [aiResponse, setAiResponse] = useState<any>(null)
  const [isAiLoading, setIsAiLoading] = useState(false)
  const [feedbackGiven, setFeedbackGiven] = useState<'good' | 'bad' | null>(null)

  const handleAiAsk = async () => {
    if (!aiQuery.trim()) return

    if (!userId.trim()) {
      alert("Please enter a User ID.")
      return
    }

    setIsAiLoading(true)
    setAiResponse(null)
    setFeedbackGiven(null)
    
    // Initial state for accumulation
    let currentResponse = {
      decision: { action: '', reason: '' },
      items: []
    }
    
    try {
      const params = new URLSearchParams({
        user_id: userId,
        query: aiQuery
      })
      const response = await fetch(`http://localhost:5001/memories?${params.toString()}`, {
        method: 'GET',
      })

      if (!response.ok) {
        const errorData = await response.json()
        alert(`Failed to get response: ${errorData.error || response.statusText}`)
        setIsAiLoading(false)
        return
      }

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()
      
      if (!reader) {
        setIsAiLoading(false)
        return
      }

      let buffer = ''
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        
        const chunk = decoder.decode(value, { stream: true })
        buffer += chunk
        
        const lines = buffer.split('\n\n')
        buffer = lines.pop() || ''
        
        for (const line of lines) {
          if (line.startsWith('event: ')) {
            const [eventType, ...dataParts] = line.split('\n')
            const eventName = eventType.replace('event: ', '').trim()
            const dataLine = dataParts.find(p => p.startsWith('data: '))
            
            if (dataLine) {
              const dataStr = dataLine.replace('data: ', '')
              
              if (eventName === 'memories') {
                const memoriesData = JSON.parse(dataStr)
                currentResponse = { ...currentResponse, ...memoriesData }
                setAiResponse({ ...currentResponse })
              } else if (eventName === 'token') {
                const token = JSON.parse(dataStr)
                currentResponse.decision.reason += token
                
                // Try to extract ACTION from the reason text as it streams
                const actionMatch = currentResponse.decision.reason.match(/ACTION:\s*(BUY|SELL|HOLD)/i)
                if (actionMatch) {
                  currentResponse.decision.action = actionMatch[1].toUpperCase()
                }
                
                // Clean up the reason text to hide the ACTION line if desired, 
                // but for now let's just show raw stream and maybe highlight action separately
                setAiResponse({ ...currentResponse })
              } else if (eventName === 'error') {
                 console.error("Stream error:", dataStr)
              }
            }
          }
        }
      }
      
      // Final cleanup of reason text to remove "ACTION: ..." line if present at start
      if (currentResponse.decision.reason.includes('ACTION:')) {
         const parts = currentResponse.decision.reason.split('REASON:')
         if (parts.length > 1) {
             currentResponse.decision.reason = parts[1].trim()
         }
         setAiResponse({ ...currentResponse })
      }

    } catch (error) {
      console.error("Error calling memories API:", error)
      alert("An error occurred while asking AI.")
    } finally {
      setIsAiLoading(false)
    }
  }

  const renderContent = () => {
    switch (currentView) {
      case 'input-memory':
        return (
          <Card className="w-[450px]">
            <CardHeader>
              <CardTitle>Input Memory</CardTitle>
              <CardDescription>Record new memories or information.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid w-full items-center gap-4">
                <div className="flex flex-col space-y-1.5">
                  <Select value={selectedCurrency} onValueChange={setSelectedCurrency}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select Currency Pair" />
                    </SelectTrigger>
                    <SelectContent>
                      {CURRENCY_PAIRS.map((pair) => (
                        <SelectItem key={pair} value={pair}>
                          {pair}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="flex flex-col space-y-1.5">
                  <Textarea 
                    placeholder="Input information want to memorize." 
                    className="min-h-[150px]"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                  />
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex justify-end">
              <Button onClick={handleSend} disabled={isSending}>
                {isSending ? "Sending..." : "Send"}
              </Button>
            </CardFooter>
          </Card>
        )
      case 'ask-ai':
        return (
          <Card className="w-[800px] h-[700px] flex flex-col">
            <CardHeader>
              <CardTitle>Ask to AI</CardTitle>
              <CardDescription>Chat with your AI assistant to get financial advice.</CardDescription>
            </CardHeader>
            <CardContent className="flex-1 overflow-y-auto">
              {aiResponse ? (
                <div className="space-y-6">
                  {aiResponse.decision && (
                    <div className={`p-4 rounded-lg border flex flex-col gap-4 ${
                      aiResponse.decision.action === 'BUY' ? 'bg-green-50 border-green-200' :
                      aiResponse.decision.action === 'SELL' ? 'bg-red-50 border-red-200' :
                      'bg-yellow-50 border-yellow-200'
                    }`}>
                      <div>
                        <div className="flex items-center gap-2 mb-2">
                          <span className="font-bold text-lg">Recommendation:</span>
                          <span className={`font-black text-xl ${
                            aiResponse.decision.action === 'BUY' ? 'text-green-700' :
                            aiResponse.decision.action === 'SELL' ? 'text-red-700' :
                            'text-yellow-700'
                          }`}>{aiResponse.decision.action}</span>
                        </div>
                        <p className="text-sm text-gray-700">{aiResponse.decision.reason}</p>
                      </div>

                      <div className="flex items-center gap-2 pt-2 border-t border-black/5">
                        <span className="text-sm font-medium opacity-80 mr-auto">Was this analysis helpful?</span>
                        {feedbackGiven ? (
                          <span className="text-sm font-medium">Thanks for your feedback!</span>
                        ) : (
                          <div className="flex gap-2">
                            <Button
                              variant="outline"
                              className="gap-2 bg-white/50 hover:bg-white text-green-700 border-green-200 hover:border-green-300"
                              onClick={() => setFeedbackGiven('good')}
                            >
                              <ThumbsUp className="h-4 w-4" />
                              Good
                            </Button>
                            <Button
                              variant="outline"
                              className="gap-2 bg-white/50 hover:bg-white text-red-700 border-red-200 hover:border-red-300"
                              onClick={() => setFeedbackGiven('bad')}
                            >
                              <ThumbsDown className="h-4 w-4" />
                              Bad
                            </Button>
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {aiResponse.items && aiResponse.items.length > 0 && (
                    <div>
                      <h3 className="font-semibold mb-3">Relevant Memories</h3>
                      <div className="space-y-3">
                        {aiResponse.items.map((item: any, index: number) => (
                          <div key={index} className="bg-slate-50 p-3 rounded border text-sm">
                            <p>{item.content}</p>
                            <span className="text-xs text-muted-foreground mt-1 block capitalize">
                              Type: {item.memory_type}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="h-full flex flex-col justify-center items-center text-muted-foreground">
                  <p>Ask a question about currency pairs (e.g., "Should I buy USD/JPY?").</p>
                </div>
              )}
            </CardContent>
            <CardFooter>
              <div className="flex w-full items-center space-x-2">
                <Input 
                  type="text" 
                  placeholder="Ask something..." 
                  value={aiQuery}
                  onChange={(e) => setAiQuery(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleAiAsk()}
                />
                <Button onClick={handleAiAsk} disabled={isAiLoading}>
                  {isAiLoading ? "Thinking..." : "Send"}
                </Button>
              </div>
            </CardFooter>
          </Card>
        )
      case 'profile':
        return (
          <Card className="w-[450px]">
            <CardHeader>
              <CardTitle>Profile</CardTitle>
              <CardDescription>Manage your profile settings.</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">Profile settings content goes here.</p>
            </CardContent>
          </Card>
        )
      case 'settings':
        return (
          <Card className="w-[450px]">
            <CardHeader>
              <CardTitle>Settings</CardTitle>
              <CardDescription>Configure application settings.</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">Application settings content goes here.</p>
            </CardContent>
          </Card>
        )
      default:
        return <div>Select a menu item</div>
    }
  }

  return (
    <div className="flex min-h-screen w-full bg-background">
      <Sidebar 
        currentView={currentView} 
        onNavigate={setCurrentView} 
        userId={userId}
        onUserIdChange={setUserId}
      />
      <main className="flex-1 p-8 flex items-center justify-center bg-gray-50/50">
        {renderContent()}
      </main>
    </div>
  )
}

export default App
