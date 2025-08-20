import React, { useState } from 'react';
import { 
  Button, 
  Paper, 
  Typography, 
  Box, 
  Alert,
  IconButton
} from '@mui/material';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import ChatIcon from '@mui/icons-material/Chat';
import SettingsIcon from '@mui/icons-material/Settings';

import VirtualAssistant from './VirtualAssistant';

const VoiceQueryForm = ({ onQueryComplete }) => {
  const [isAssistantOpen, setIsAssistantOpen] = useState(false);
  const [error, setError] = useState('');

  const handleAssistantOpen = () => {
    setIsAssistantOpen(true);
  };

  const handleAssistantClose = () => {
    setIsAssistantOpen(false);
  };

  const handleAssistantComplete = (result) => {
    if (onQueryComplete) {
      onQueryComplete(result);
    }
    setIsAssistantOpen(false);
  };

  return (
    <>
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Virtual Assistant
        </Typography>
        
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 3 }}>
          <Box sx={{ 
            display: 'flex', 
            flexDirection: 'column',
            alignItems: 'center',
            gap: 2,
            p: 4,
            borderRadius: 3,
            background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)',
            border: '1px solid rgba(102, 126, 234, 0.2)',
            width: '100%',
            maxWidth: 400
          }}>
            <Box sx={{ 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              width: 120, 
              height: 120, 
              borderRadius: '50%', 
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              mb: 2,
              boxShadow: '0 8px 32px rgba(102, 126, 234, 0.3)'
            }}>
              <SmartToyIcon sx={{ fontSize: 60, color: 'white' }} />
            </Box>
            
            <Typography variant="h5" sx={{ mb: 1, textAlign: 'center', fontWeight: 600 }}>
              AI Virtual Assistant
            </Typography>
            
            <Typography variant="body1" sx={{ textAlign: 'center', mb: 3, color: 'text.secondary' }}>
              Chat with our intelligent assistant using voice or text. 
              Get instant troubleshooting help with speech recognition and text-to-speech.
            </Typography>

            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', justifyContent: 'center' }}>
              <Button
                variant="contained"
                size="large"
                onClick={handleAssistantOpen}
                startIcon={<ChatIcon />}
                sx={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  color: 'white',
                  px: 4,
                  py: 1.5,
                  borderRadius: 2,
                  textTransform: 'none',
                  fontSize: '1.1rem',
                  fontWeight: 600,
                  boxShadow: '0 4px 16px rgba(102, 126, 234, 0.3)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%)',
                    boxShadow: '0 6px 20px rgba(102, 126, 234, 0.4)',
                    transform: 'translateY(-2px)'
                  },
                  transition: 'all 0.3s ease'
                }}
              >
                Start Chat
              </Button>
              
              <Button
                variant="outlined"
                size="large"
                startIcon={<SettingsIcon />}
                sx={{
                  borderColor: 'rgba(102, 126, 234, 0.5)',
                  color: 'primary.main',
                  px: 4,
                  py: 1.5,
                  borderRadius: 2,
                  textTransform: 'none',
                  fontSize: '1.1rem',
                  fontWeight: 600,
                  '&:hover': {
                    borderColor: 'primary.main',
                    backgroundColor: 'rgba(102, 126, 234, 0.05)'
                  }
                }}
              >
                Settings
              </Button>
            </Box>
          </Box>
        </Box>

        <Box sx={{ 
          p: 2, 
          borderRadius: 2, 
          background: 'rgba(76, 175, 80, 0.1)', 
          border: '1px solid rgba(76, 175, 80, 0.2)' 
        }}>
          <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1, color: 'success.main' }}>
            ✨ Features Available:
          </Typography>
          <Box component="ul" sx={{ m: 0, pl: 2, color: 'text.secondary' }}>
            <li>Voice recognition for hands-free interaction</li>
            <li>Text-to-speech for audio responses</li>
            <li>Real-time conversation with AI</li>
            <li>Intelligent troubleshooting assistance</li>
            <li>Multi-language support</li>
            <li>Context-aware responses</li>
          </Box>
        </Box>
        
        {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      </Paper>

      <VirtualAssistant
        isOpen={isAssistantOpen}
        onClose={handleAssistantClose}
        onQueryComplete={handleAssistantComplete}
      />
    </>
  );
};

export default VoiceQueryForm;
