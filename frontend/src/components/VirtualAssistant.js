import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Paper,
  Typography,
  IconButton,
  TextField,
  Button,
  Avatar,
  Chip,
  CircularProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Divider,
  Fade,
  Slide,
  Zoom,
  useTheme,
  alpha
} from '@mui/material';
import {
  Mic as MicIcon,
  MicOff as MicOffIcon,
  Send as SendIcon,
  VolumeUp as VolumeUpIcon,
  VolumeOff as VolumeOffIcon,
  SmartToy as AssistantIcon,
  Settings as SettingsIcon,
  Close as CloseIcon,
  AutoFixHigh as MagicIcon,
  Psychology as BrainIcon,
  Clear as ClearIcon
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';

const VirtualAssistant = ({ onQueryComplete, isOpen, onClose }) => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [speechEnabled, setSpeechEnabled] = useState(true);
  const [showSettings, setShowSettings] = useState(false);
  const [waveAnimation, setWaveAnimation] = useState(false);
  
  const recognitionRef = useRef(null);
  const synthesisRef = useRef(null);
  const messagesEndRef = useRef(null);
  const sessionId = useRef(null);
  const theme = useTheme();

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  // Initialize speech recognition
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = true;
      recognitionRef.current.interimResults = true;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onstart = () => {
        setIsListening(true);
        setWaveAnimation(true);
        setError('');
      };

      recognitionRef.current.onresult = (event) => {
        let finalTranscript = '';
        let interimTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }

        setTranscript(finalTranscript + interimTranscript);
      };

      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setError(`Speech recognition error: ${event.error}`);
        setIsListening(false);
        setWaveAnimation(false);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
        setWaveAnimation(false);
      };
    } else {
      setError('Speech recognition not supported in this browser');
    }

    // Initialize speech synthesis
    if ('speechSynthesis' in window) {
      synthesisRef.current = window.speechSynthesis;
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, []);

  const startListening = () => {
    if (recognitionRef.current) {
      setTranscript('');
      recognitionRef.current.start();
    }
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
  };

  const speak = (text) => {
    if (synthesisRef.current && speechEnabled) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.9;
      utterance.pitch = 1.1;
      utterance.volume = 0.8;
      
      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      
      synthesisRef.current.speak(utterance);
    }
  };

  const handleSendMessage = async (text = inputText) => {
    if (!text.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: text,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setTranscript('');
    setIsProcessing(true);
    setError('');

    try {
      const aiResponse = await generateAIResponse(text);
      
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        text: aiResponse,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
      speak(aiResponse);

      if (onQueryComplete) {
        onQueryComplete({
          query_id: Date.now(),
          solution: {
            issue: "Virtual Assistant Response",
            possible_causes: [],
            recommended_steps: [{ step_number: 1, description: aiResponse }],
            external_sources: []
          }
        });
      }

    } catch (err) {
      setError('Error processing your message. Please try again.');
      console.error('Error processing message:', err);
    } finally {
      setIsProcessing(false);
    }
  };

  const generateAIResponse = async (userInput) => {
    try {
      // Call the virtual assistant API
              const response = await fetch('http://localhost:8000/api/v1/query/assistant/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: userInput,
          user_id: 'virtual_assistant_user',
          session_id: sessionId.current,
          input_type: 'text'
        })
      });

      if (!response.ok) {
        throw new Error('Failed to get AI response');
      }

      const result = await response.json();
      
      if (result.success && result.result) {
        const solution = result.result.solution;
        const followUpQuestions = result.result.follow_up_questions || [];
        
        // Store session ID for future requests
        if (result.result.session_id) {
          sessionId.current = result.result.session_id;
        }
        
        // Format the response
        let responseText = `I've analyzed your issue: "${solution.issue}". Here's what I recommend:\n\n`;
        
        if (solution.recommended_steps) {
          solution.recommended_steps.forEach((step, index) => {
            responseText += `${index + 1}. ${step.description}\n`;
          });
        }
        

        
        // Add follow-up questions if available
        if (followUpQuestions.length > 0) {
          responseText += `\n\nFollow-up questions:\n`;
          followUpQuestions.forEach((question, index) => {
            responseText += `• ${question}\n`;
          });
        }
        
        return responseText;
      } else {
        return "I understand your issue. Let me help you troubleshoot this step by step.";
      }
    } catch (error) {
      console.error('Error getting AI response:', error);
      return "I'm having trouble processing your request right now. Please try again.";
    }
  };

  // Handle voice input and convert to text
  const handleVoiceInput = async () => {
    if (isListening) {
      stopListening();
      // Process the transcribed text
      if (transcript.trim()) {
        await handleSendMessage(transcript);
      }
    } else {
      startListening();
    }
  };



  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const clearMessages = () => {
    setMessages([]);
  };

  const [quickActions, setQuickActions] = useState([
    { label: "System Diagnostics", prompt: "Run a full system diagnostic check" },
    { label: "Error Analysis", prompt: "Analyze recent error logs" },
    { label: "Performance Tips", prompt: "Provide performance optimization tips" },
    { label: "Troubleshooting", prompt: "Help me troubleshoot common issues" }
  ]);

  // Load quick actions from API
  useEffect(() => {
    const loadQuickActions = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/query/assistant/quick-actions');
        if (response.ok) {
          const result = await response.json();
          if (result.success && result.quick_actions) {
            const actions = Object.entries(result.quick_actions).map(([key, action]) => ({
              label: action.title,
              prompt: action.description,
              steps: action.steps
            }));
            setQuickActions(actions);
          }
        }
      } catch (error) {
        console.error('Error loading quick actions:', error);
      }
    };

    loadQuickActions();
  }, []);

  return (
    <Dialog
      open={isOpen}
      onClose={onClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: {
          background: 'linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)',
          borderRadius: 4,
          border: '1px solid rgba(255, 255, 255, 0.15)',
          backdropFilter: 'blur(12px)',
          boxShadow: '0 20px 40px rgba(0, 0, 0, 0.4)',
          overflow: 'hidden'
        }
      }}
    >
      <DialogTitle sx={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        color: 'white',
        background: 'linear-gradient(90deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        py: 2,
        px: 3
      }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <motion.div
            animate={{ 
              scale: waveAnimation ? [1, 1.1, 1] : 1,
              rotate: waveAnimation ? [0, -5, 5, 0] : 0
            }}
            transition={{ duration: 0.5, repeat: waveAnimation ? Infinity : 0 }}
          >
            <Avatar sx={{ 
              bgcolor: 'primary.main',
              width: 44,
              height: 44,
              boxShadow: '0 0 20px rgba(100, 181, 246, 0.6)'
            }}>
              <AssistantIcon />
            </Avatar>
          </motion.div>
          <Box>
            <Typography variant="h6" fontWeight="600">
              Neuro Assistant
            </Typography>
            <Typography variant="caption" sx={{ opacity: 0.7 }}>
              AI-powered troubleshooting companion
            </Typography>
          </Box>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
            <IconButton 
              onClick={() => setShowSettings(true)} 
              sx={{ 
                color: 'white',
                background: 'rgba(255, 255, 255, 0.1)',
                '&:hover': { background: 'rgba(255, 255, 255, 0.2)' }
              }}
            >
              <SettingsIcon />
            </IconButton>
          </motion.div>
          <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
            <IconButton 
              onClick={onClose} 
              sx={{ 
                color: 'white',
                background: 'rgba(255, 255, 255, 0.1)',
                '&:hover': { background: 'rgba(255, 255, 255, 0.2)' }
              }}
            >
              <CloseIcon />
            </IconButton>
          </motion.div>
        </Box>
      </DialogTitle>

      <DialogContent sx={{ p: 0, minHeight: 500 }}>
        {/* Messages Area */}
        <Box sx={{ 
          height: 350, 
          overflowY: 'auto', 
          p: 3,
          background: 'radial-gradient(circle at top right, rgba(100, 181, 246, 0.1) 0%, transparent 50%)',
          position: 'relative'
        }}>
          {messages.length === 0 && (
            <Fade in={true} timeout={1000}>
              <Box sx={{ 
                textAlign: 'center', 
                mt: 8,
                color: 'rgba(255, 255, 255, 0.6)'
              }}>
                <BrainIcon sx={{ fontSize: 64, mb: 2, opacity: 0.5 }} />
                <Typography variant="h6" gutterBottom>
                  How can I assist you today?
                </Typography>
                <Typography variant="body2">
                  Ask me anything about system issues, errors, or troubleshooting
                </Typography>
              </Box>
            </Fade>
          )}

          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -20, scale: 0.95 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
              >
                <Box sx={{ 
                  display: 'flex', 
                  justifyContent: message.type === 'user' ? 'flex-end' : 'flex-start',
                  mb: 3
                }}>
                  <Paper sx={{
                    p: 2.5,
                    maxWidth: '75%',
                    background: message.type === 'user' 
                      ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                      : 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                    color: 'white',
                    borderRadius: 3,
                    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.2)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    position: 'relative',
                    overflow: 'hidden',
                    '&::before': {
                      content: '""',
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      right: 0,
                      height: '2px',
                      background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent)'
                    }
                  }}>
                    <Typography variant="body1" sx={{ lineHeight: 1.6 }}>
                      {message.text}
                    </Typography>
                    <Typography variant="caption" sx={{ 
                      opacity: 0.7, 
                      display: 'block', 
                      mt: 1.5,
                      fontSize: '0.7rem'
                    }}>
                      {message.timestamp.toLocaleTimeString()}
                    </Typography>
                  </Paper>
                </Box>
              </motion.div>
            ))}
          </AnimatePresence>

          {isProcessing && (
            <Box sx={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: 2, 
              p: 2,
              background: 'rgba(255, 255, 255, 0.05)',
              borderRadius: 2,
              border: '1px solid rgba(255, 255, 255, 0.1)'
            }}>
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
              >
                <MagicIcon color="primary" />
              </motion.div>
              <Typography variant="body2" color="primary.light">
                Analyzing your request...
              </Typography>
            </Box>
          )}
          <div ref={messagesEndRef} />
        </Box>

        {/* Quick Actions */}
        <Box sx={{ 
          p: 2, 
          background: 'rgba(0, 0, 0, 0.3)',
          borderTop: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
          <Typography variant="caption" sx={{ 
            color: 'rgba(255, 255, 255, 0.6)', 
            display: 'block', 
            mb: 1,
            ml: 1
          }}>
            QUICK ACTIONS
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {quickActions.map((action, index) => (
              <motion.div
                key={action.label}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <Chip
                  label={action.label}
                  onClick={() => handleSendMessage(action.prompt)}
                  sx={{ 
                    background: 'linear-gradient(45deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.1) 100%)',
                    color: 'white',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    '&:hover': { 
                      background: 'linear-gradient(45deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.15) 100%)',
                    }
                  }}
                />
              </motion.div>
            ))}
          </Box>
        </Box>

        {/* Input Area */}
        <Box sx={{ 
          p: 3, 
          background: 'rgba(0, 0, 0, 0.4)',
          borderTop: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
          {error && (
            <Slide in={!!error} direction="up">
              <Alert 
                severity="error" 
                sx={{ 
                  mb: 2,
                  background: 'rgba(244, 67, 54, 0.2)',
                  color: 'white',
                  border: '1px solid rgba(244, 67, 54, 0.3)'
                }}
                onClose={() => setError('')}
              >
                {error}
              </Alert>
            </Slide>
          )}

          {/* Voice Input Display */}
          {transcript && (
            <Zoom in={!!transcript}>
              <Paper sx={{ 
                p: 2, 
                mb: 2, 
                background: 'rgba(255, 255, 255, 0.08)',
                border: '1px solid rgba(255, 255, 255, 0.15)',
                borderRadius: 2
              }}>
                <Typography variant="body2" color="primary.light" sx={{ mb: 1 }}>
                  🎤 Listening...
                </Typography>
                <Typography variant="body1" color="white">
                  {transcript}
                </Typography>
              </Paper>
            </Zoom>
          )}

          {/* Input Controls */}
          <Box sx={{ display: 'flex', gap: 1.5, alignItems: 'flex-end' }}>
            <TextField
              fullWidth
              multiline
              maxRows={3}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Describe your issue or ask for help..."
              variant="outlined"
              sx={{
                '& .MuiOutlinedInput-root': {
                  color: 'white',
                  '& fieldset': {
                    borderColor: 'rgba(255, 255, 255, 0.2)',
                    borderRadius: 2
                  },
                  '&:hover fieldset': {
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                  },
                  '&.Mui-focused fieldset': {
                    borderColor: 'primary.main',
                    boxShadow: '0 0 0 2px rgba(100, 181, 246, 0.2)'
                  },
                  '& input': {
                    color: 'white',
                  },
                  '& textarea': {
                    color: 'white',
                  },
                  background: 'rgba(255, 255, 255, 0.05)',
                  borderRadius: 2
                },
                '& .MuiInputLabel-root': {
                  color: 'rgba(255, 255, 255, 0.6)',
                },
              }}
            />
            
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <IconButton
                  onClick={handleVoiceInput}
                  sx={{
                    bgcolor: isListening ? 'error.main' : 'primary.main',
                    color: 'white',
                    '&:hover': {
                      bgcolor: isListening ? 'error.dark' : 'primary.dark',
                    },
                    width: 50,
                    height: 50
                  }}
                >
                  {isListening ? <MicOffIcon /> : <MicIcon />}
                </IconButton>
              </motion.div>

              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <IconButton
                  onClick={() => setSpeechEnabled(!speechEnabled)}
                  sx={{
                    bgcolor: speechEnabled ? 'success.main' : 'grey.700',
                    color: 'white',
                    '&:hover': {
                      bgcolor: speechEnabled ? 'success.dark' : 'grey.600',
                    },
                    width: 50,
                    height: 50
                  }}
                >
                  {speechEnabled ? <VolumeUpIcon /> : <VolumeOffIcon />}
                </IconButton>
              </motion.div>

              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  variant="contained"
                  onClick={() => handleSendMessage()}
                  disabled={!inputText.trim() && !transcript.trim()}
                  sx={{
                    bgcolor: 'primary.main',
                    color: 'white',
                    minWidth: 50,
                    height: 50,
                    borderRadius: 2,
                    '&:hover': {
                      bgcolor: 'primary.dark',
                      transform: 'translateY(-2px)',
                      boxShadow: '0 4px 12px rgba(100, 181, 246, 0.4)'
                    },
                    '&.Mui-disabled': {
                      bgcolor: 'grey.700',
                      color: 'grey.500'
                    }
                  }}
                >
                  <SendIcon />
                </Button>
              </motion.div>
            </Box>
          </Box>
        </Box>
      </DialogContent>

      {/* Settings Dialog */}
      <Dialog 
        open={showSettings} 
        onClose={() => setShowSettings(false)}
        PaperProps={{
          sx: {
            background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
            color: 'white',
            borderRadius: 3
          }
        }}
      >
        <DialogTitle sx={{ borderBottom: '1px solid rgba(255, 255, 255, 0.1)' }}>
          Assistant Settings
        </DialogTitle>
        <DialogContent>
          <List>
            <ListItem>
              <ListItemAvatar>
                <Avatar sx={{ bgcolor: 'primary.main' }}>
                  <VolumeUpIcon />
                </Avatar>
              </ListItemAvatar>
              <ListItemText 
                primary="Speech Synthesis" 
                secondary="Enable text-to-speech for responses"
              />
              <IconButton
                onClick={() => setSpeechEnabled(!speechEnabled)}
                color={speechEnabled ? 'primary' : 'default'}
                sx={{ color: 'white' }}
              >
                {speechEnabled ? <VolumeUpIcon /> : <VolumeOffIcon />}
              </IconButton>
            </ListItem>
            <Divider sx={{ bgcolor: 'rgba(255, 255, 255, 0.1)' }} />
            <ListItem>
              <ListItemAvatar>
                <Avatar sx={{ bgcolor: 'secondary.main' }}>
                  <MicIcon />
                </Avatar>
              </ListItemAvatar>
              <ListItemText 
                primary="Voice Recognition" 
                secondary="Enable speech-to-text input"
              />
              <Chip 
                label={recognitionRef.current ? "Available" : "Not Available"}
                color={recognitionRef.current ? "success" : "error"}
                size="small"
                sx={{ color: 'white' }}
              />
            </ListItem>
          </List>
        </DialogContent>
        <DialogActions sx={{ borderTop: '1px solid rgba(255, 255, 255, 0.1)' }}>
          <Button 
            onClick={() => setShowSettings(false)}
            sx={{ color: 'white' }}
          >
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Dialog>
  );
};

export default VirtualAssistant;