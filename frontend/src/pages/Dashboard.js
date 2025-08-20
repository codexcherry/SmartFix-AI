import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Paper, 
  Tabs, 
  Tab,
  AppBar,
  Toolbar,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  useTheme,
  useMediaQuery,
  Avatar,
  Fade,
  Zoom,
  Card,
  CardContent,
  Grid,
  Chip,
  alpha,
  styled
} from '@mui/material';
import TextQueryForm from '../components/TextQueryForm';
import ImageQueryForm from '../components/ImageQueryForm';
import VoiceQueryForm from '../components/VoiceQueryForm';
import LogFileForm from '../components/LogFileForm';
import SolutionDisplay from '../components/SolutionDisplay';
import DeviceAnalyzer from '../components/DeviceAnalyzer';
import HistoryIcon from '@mui/icons-material/History';
import HomeIcon from '@mui/icons-material/Home';
import SettingsIcon from '@mui/icons-material/Settings';
import MenuIcon from '@mui/icons-material/Menu';
import TextFieldsIcon from '@mui/icons-material/TextFields';
import ImageIcon from '@mui/icons-material/Image';
import MicIcon from '@mui/icons-material/Mic';
import DescriptionIcon from '@mui/icons-material/Description';
import ComputerIcon from '@mui/icons-material/Computer';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import PersonIcon from '@mui/icons-material/Person';
import NotificationsIcon from '@mui/icons-material/Notifications';
import CloseIcon from '@mui/icons-material/Close';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import { motion, AnimatePresence } from 'framer-motion';

// Styled components for Apple-inspired UI
const GlassPaper = styled(Paper)(({ theme }) => ({
  background: 'rgba(0, 0, 0, 0.8)',
  backdropFilter: 'blur(10px)',
  borderRadius: 16,
  border: `1px solid rgba(255, 255, 255, 0.1)`,
  boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.3)'
}));

const FloatingCard = styled(Card)(({ theme }) => ({
  borderRadius: 16,
  overflow: 'hidden',
  transition: 'all 0.3s ease',
  background: 'rgba(0, 0, 0, 0.8)',
  boxShadow: '0 4px 20px rgba(0, 0, 0, 0.3)',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: '0 12px 32px rgba(0, 0, 0, 0.5)'
  }
}));

const StyledTab = styled(Tab)(({ theme }) => ({
  minHeight: 64,
  borderRadius: 12,
  margin: '0 4px',
  transition: 'all 0.3s ease',
  '&.Mui-selected': {
    backgroundColor: alpha(theme.palette.primary.main, 0.1),
    color: theme.palette.primary.main,
  }
}));

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [solution, setSolution] = useState(null);
  const [queryId, setQueryId] = useState(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [userHistory, setUserHistory] = useState([]);
  
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  useEffect(() => {
    const fetchUserHistory = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/query/history/test_user');
        if (response.ok) {
          const data = await response.json();
          setUserHistory(data);
        }
      } catch (error) {
        console.error('Error fetching user history:', error);
      }
    };

    fetchUserHistory();
  }, [solution]);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleQueryComplete = (result) => {
    setSolution(result.solution);
    setQueryId(result.query_id);
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  };

  const toggleDrawer = (open) => (event) => {
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
      return;
    }
    setDrawerOpen(open);
  };

  const clearSolution = () => {
    setSolution(null);
    setQueryId(null);
  };

  const drawerItems = [
    { text: 'Home', icon: <HomeIcon /> },
    { text: 'History', icon: <HistoryIcon /> },
    { text: 'Settings', icon: <SettingsIcon /> },
  ];

  // Reordered tabs with Device Analysis first
  const tabLabels = ['Device Analysis', 'Text', 'Image', 'Voice', 'Logs'];
  const tabIcons = [
    <ComputerIcon />,
    <TextFieldsIcon />,
    <ImageIcon />,
    <MicIcon />,
    <DescriptionIcon />
  ];

  return (
    <Box sx={{ 
      flexGrow: 1, 
      minHeight: '100vh', 
      display: 'flex', 
      flexDirection: 'column', 
      bgcolor: 'background.default',
      background: '#000000',
      position: 'relative',
      overflow: 'hidden',
      '&::before': {
        content: '""',
        position: 'absolute',
        width: '100%',
        height: '100%',
        background: 'transparent',
        zIndex: 0
      }
    }}>
      <AppBar 
        position="fixed" 
        elevation={0}
        sx={{ 
          bgcolor: alpha(theme.palette.background.paper, 0.8),
          backdropFilter: 'blur(10px)',
          borderBottom: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
          zIndex: theme.zIndex.drawer + 1
        }}
      >
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            aria-label="menu"
            onClick={toggleDrawer(true)}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Typography variant="h6" component="div" sx={{ 
              flexGrow: 1, 
              fontWeight: 700,
              background: 'linear-gradient(45deg, #667eea 0%, #764ba2 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent'
            }}>
              SmartFix AI
            </Typography>
          </motion.div>
          
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.95 }}>
              <IconButton color="inherit" sx={{ mr: 1 }}>
                <DarkModeIcon />
              </IconButton>
            </motion.div>
            
            <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.95 }}>
              <IconButton color="inherit" sx={{ mr: 1 }}>
                <NotificationsIcon />
              </IconButton>
            </motion.div>
            
            <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.95 }}>
              <IconButton color="inherit">
                <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>
                  <PersonIcon fontSize="small" />
                </Avatar>
              </IconButton>
            </motion.div>
          </Box>
        </Toolbar>
      </AppBar>
      
      <Drawer 
        anchor="left" 
        open={drawerOpen} 
        onClose={toggleDrawer(false)}
        PaperProps={{
          sx: {
            width: 280,
            bgcolor: alpha(theme.palette.background.paper, 0.8),
            backdropFilter: 'blur(10px)',
            borderRight: `1px solid ${alpha(theme.palette.divider, 0.1)}`
          }
        }}
      >
        <Box
          sx={{ width: 280, height: '100%' }}
          role="presentation"
          onClick={toggleDrawer(false)}
          onKeyDown={toggleDrawer(false)}
        >
          <Box sx={{ p: 3, display: 'flex', alignItems: 'center', flexDirection: 'column' }}>
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.1, type: "spring", stiffness: 200, damping: 15 }}
            >
              <Avatar sx={{ width: 64, height: 64, mb: 2, bgcolor: 'primary.main' }}>
                <PersonIcon />
              </Avatar>
            </motion.div>
            <Typography variant="h6" gutterBottom>User Name</Typography>
            <motion.div whileHover={{ scale: 1.05 }}>
              <Chip label="Premium" size="small" color="primary" />
            </motion.div>
          </Box>
          
          <Divider sx={{ my: 1 }} />
          
          <List sx={{ px: 2 }}>
            {drawerItems.map((item, index) => (
              <motion.div
                key={item.text}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <ListItem button sx={{ borderRadius: 2, mb: 0.5 }}>
                  <ListItemIcon>
                    {item.icon}
                  </ListItemIcon>
                  <ListItemText primary={item.text} />
                </ListItem>
              </motion.div>
            ))}
          </List>
        </Box>
      </Drawer>
      
      <Box component="main" sx={{ flexGrow: 1, pt: 10, pb: 4, position: 'relative', zIndex: 1 }}>
        <Container maxWidth="lg">
          <Grid container spacing={3}>
            <Grid item xs={12} md={solution ? 7 : 12}>
              <AnimatePresence>
                {solution && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                  >
                    <IconButton 
                      onClick={clearSolution} 
                      sx={{ 
                        mb: 2, 
                        bgcolor: 'rgba(0, 0, 0, 0.8)',
                        boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
                        '&:hover': { bgcolor: 'action.hover' }
                      }}
                    >
                      <CloseIcon />
                    </IconButton>
                  </motion.div>
                )}
              </AnimatePresence>
              
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <GlassPaper elevation={0}>
                  <Tabs
                    value={activeTab}
                    onChange={handleTabChange}
                    indicatorColor="primary"
                    textColor="primary"
                    variant={isMobile ? "scrollable" : "fullWidth"}
                    scrollButtons={false}
                    aria-label="query input tabs"
                    sx={{
                      '& .MuiTabs-indicator': {
                        borderRadius: 2,
                        height: 3
                      }
                    }}
                  >
                    {tabLabels.map((label, index) => (
                      <StyledTab 
                        key={label} 
                        label={!isMobile ? label : ''} 
                        icon={tabIcons[index]} 
                        iconPosition={isMobile ? 'top' : 'start'}
                      />
                    ))}
                  </Tabs>
                  
                  <Box sx={{ p: 3 }}>
                    <Fade in={activeTab === 0} timeout={300}>
                      <Box sx={{ display: activeTab === 0 ? 'block' : 'none' }}>
                        <DeviceAnalyzer onQueryComplete={handleQueryComplete} setLoading={setLoading} />
                      </Box>
                    </Fade>
                    
                    <Fade in={activeTab === 1} timeout={300}>
                      <Box sx={{ display: activeTab === 1 ? 'block' : 'none' }}>
                        <TextQueryForm onQueryComplete={handleQueryComplete} setLoading={setLoading} />
                      </Box>
                    </Fade>
                    
                    <Fade in={activeTab === 2} timeout={300}>
                      <Box sx={{ display: activeTab === 2 ? 'block' : 'none' }}>
                        <ImageQueryForm onQueryComplete={handleQueryComplete} setLoading={setLoading} />
                      </Box>
                    </Fade>
                    
                    <Fade in={activeTab === 3} timeout={300}>
                      <Box sx={{ display: activeTab === 3 ? 'block' : 'none' }}>
                        <VoiceQueryForm onQueryComplete={handleQueryComplete} setLoading={setLoading} />
                      </Box>
                    </Fade>
                    
                    <Fade in={activeTab === 4} timeout={300}>
                      <Box sx={{ display: activeTab === 4 ? 'block' : 'none' }}>
                        <LogFileForm onQueryComplete={handleQueryComplete} setLoading={setLoading} />
                      </Box>
                    </Fade>
                  </Box>
                </GlassPaper>
              </motion.div>
              
              {!solution && userHistory.length > 0 && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.5, delay: 0.3 }}
                >
                  <Box sx={{ mt: 4 }}>
                    <Typography variant="h6" sx={{ mb: 2, fontWeight: 600, color: 'text.primary' }}>
                      Recent Queries
                    </Typography>
                    
                    <Grid container spacing={2}>
                      {userHistory.slice(0, 3).map((query, index) => (
                        <Grid item xs={12} sm={6} md={4} key={query.id}>
                          <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.1 }}
                            whileHover={{ y: -5 }}
                          >
                            <FloatingCard 
                              elevation={1}
                              sx={{ 
                                cursor: 'pointer',
                                height: '100%',
                              }}
                              onClick={() => {
                                setSolution(query.solution);
                                setQueryId(query.id);
                              }}
                            >
                              <CardContent>
                                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                  <AnalyticsIcon color="primary" sx={{ fontSize: 16, mr: 1 }} />
                                  <Typography variant="subtitle2" noWrap>
                                    {query.solution?.issue || 'Technical Issue'}
                                  </Typography>
                                </Box>
                                <Typography variant="body2" color="text.secondary" noWrap>
                                  {query.query_content?.text?.substring(0, 60) || 'No description available'}
                                </Typography>
                              </CardContent>
                            </FloatingCard>
                          </motion.div>
                        </Grid>
                      ))}
                    </Grid>
                  </Box>
                </motion.div>
              )}
            </Grid>
            
            <AnimatePresence>
              {solution && (
                <Grid item xs={12} md={5}>
                  <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 20 }}
                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                  >
                    <SolutionDisplay solution={solution} queryId={queryId} />
                  </motion.div>
                </Grid>
              )}
            </AnimatePresence>
          </Grid>
        </Container>
      </Box>
    </Box>
  );
};

export default Dashboard;