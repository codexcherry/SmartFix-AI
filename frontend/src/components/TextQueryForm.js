import React, { useState } from 'react';
import { 
  TextField, 
  Button, 
  Typography, 
  Box, 
  CircularProgress,
  IconButton,
  Tooltip,
  Chip,
  Fade
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import ClearIcon from '@mui/icons-material/Clear';
import MicIcon from '@mui/icons-material/Mic';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';

const TextQueryForm = ({ onQueryComplete, setLoading: setParentLoading }) => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [suggestions] = useState([
    'My TV screen is flickering',
    'WiFi keeps disconnecting',
    'Smartphone battery drains quickly',
    'Laptop overheating issue'
  ]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a query');
      return;
    }
    
    setLoading(true);
    setError('');
    if (setParentLoading) setParentLoading(true);
    
    try {
      const response = await fetch('http://localhost:8000/api/v1/query/text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: 'test_user',
          input_type: 'text',
          text_query: query
        }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to process query');
      }
      
      const result = await response.json();
      setLoading(false);
      if (setParentLoading) setParentLoading(false);
      
      // Text-to-speech for the response
      if (result.solution && result.solution.issue) {
        const utterance = new SpeechSynthesisUtterance(
          `I found an issue: ${result.solution.issue}. 
           Possible causes include: ${result.solution.possible_causes.join(', ')}. 
           Here's what you can do: ${result.solution.recommended_steps.map(step => step.description).join('. ')}`
        );
        utterance.rate = 0.9;
        utterance.pitch = 1;
        window.speechSynthesis.speak(utterance);
      }
      
      if (onQueryComplete) {
        onQueryComplete(result);
      }
      
      setQuery('');
    } catch (err) {
      setLoading(false);
      if (setParentLoading) setParentLoading(false);
      setError('Error processing your query. Please try again.');
      console.error('Error submitting text query:', err);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setQuery(suggestion);
  };

  const handleClear = () => {
    setQuery('');
    setError('');
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom sx={{ fontWeight: 500, mb: 2 }}>
        What issue are you experiencing?
      </Typography>
      
      <form onSubmit={handleSubmit}>
        <Box sx={{ position: 'relative' }}>
          <TextField
            fullWidth
            variant="outlined"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Describe your issue in detail..."
            error={!!error}
            helperText={error}
            disabled={loading}
            multiline
            rows={3}
            sx={{ 
              mb: 2,
              '& .MuiOutlinedInput-root': {
                borderRadius: 2,
                backgroundColor: 'rgba(255, 255, 255, 0.05)',
                '&:hover': {
                  backgroundColor: 'rgba(255, 255, 255, 0.08)',
                },
                '&.Mui-focused': {
                  backgroundColor: 'rgba(255, 255, 255, 0.08)',
                }
              }
            }}
            InputProps={{
              endAdornment: query && (
                <IconButton 
                  size="small" 
                  onClick={handleClear}
                  sx={{ position: 'absolute', top: 8, right: 8 }}
                >
                  <ClearIcon fontSize="small" />
                </IconButton>
              )
            }}
          />
        </Box>
        
        <Box sx={{ mb: 3 }}>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
            <AutoAwesomeIcon fontSize="small" sx={{ verticalAlign: 'middle', mr: 0.5 }} />
            Suggested queries:
          </Typography>
          
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {suggestions.map((suggestion, index) => (
              <Chip
                key={index}
                label={suggestion}
                onClick={() => handleSuggestionClick(suggestion)}
                sx={{ 
                  borderRadius: 2,
                  transition: 'all 0.2s ease',
                  '&:hover': {
                    transform: 'translateY(-2px)',
                    boxShadow: '0 4px 8px rgba(0,0,0,0.2)'
                  }
                }}
              />
            ))}
          </Box>
        </Box>
        
        <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
          <Tooltip title="Use voice input">
            <IconButton 
              color="primary"
              sx={{ 
                borderRadius: 2,
                border: '1px solid rgba(33, 150, 243, 0.5)',
              }}
            >
              <MicIcon />
            </IconButton>
          </Tooltip>
          
          <Button 
            type="submit" 
            variant="contained" 
            color="primary"
            disabled={loading || !query.trim()}
            endIcon={loading ? <CircularProgress size={20} color="inherit" /> : <SendIcon />}
            sx={{ 
              px: 4,
              py: 1,
              borderRadius: 2,
              background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
            }}
          >
            {loading ? 'Processing...' : 'Submit'}
          </Button>
        </Box>
      </form>
    </Box>
  );
};

export default TextQueryForm;