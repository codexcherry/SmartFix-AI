import uuid
import logging
import re
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import numpy as np

# Download required NLTK data (run once)
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    pass

logger = logging.getLogger(__name__)

@dataclass
class QueryIntent:
    """Represents the intent classification of a user query"""
    intent: str
    confidence: float
    entities: Dict[str, Any]
    sentiment: str
    urgency: str

@dataclass
class AssistantResponse:
    """Structured response from the virtual assistant"""
    query_id: str
    session_id: str
    response_text: str
    solution_steps: List[Dict[str, Any]]
    confidence_score: float
    follow_up_questions: List[str]
    suggested_actions: List[str]
    metadata: Dict[str, Any]

class NLPProcessor:
    """Advanced NLP processing engine"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.intents_trained = False
        self._initialize_intent_patterns()
    
    def _initialize_intent_patterns(self):
        """Initialize intent recognition patterns"""
        self.intent_patterns = {
            'technical_issue': {
                'keywords': ['error', 'crash', 'problem', 'issue', 'bug', 'broken', 'not working', 'fail'],
                'phrases': ['having trouble', 'not responding', 'keeps crashing', 'error message'],
                'weight': 1.0
            },
            'how_to': {
                'keywords': ['how', 'tutorial', 'guide', 'steps', 'instructions', 'setup'],
                'phrases': ['how to', 'how do i', 'can you show me', 'walk me through'],
                'weight': 0.9
            },
            'troubleshooting': {
                'keywords': ['fix', 'solve', 'troubleshoot', 'repair', 'debug'],
                'phrases': ['how to fix', 'need help with', 'cant get it to work'],
                'weight': 1.0
            },
            'information': {
                'keywords': ['what', 'explain', 'tell me', 'information', 'details'],
                'phrases': ['what is', 'can you explain', 'tell me about'],
                'weight': 0.7
            },
            'software': {
                'keywords': ['application', 'program', 'software', 'app', 'install', 'update'],
                'phrases': ['software issue', 'app not working', 'program crash'],
                'weight': 0.8
            },
            'network': {
                'keywords': ['wifi', 'internet', 'connection', 'network', 'router', 'modem'],
                'phrases': ['internet not working', 'wifi problems', 'network issues'],
                'weight': 0.9
            },
            'hardware': {
                'keywords': ['computer', 'laptop', 'device', 'hardware', 'screen', 'keyboard'],
                'phrases': ['hardware problem', 'device not working', 'computer issue'],
                'weight': 0.8
            },
            'performance': {
                'keywords': ['slow', 'speed', 'performance', 'lag', 'freeze', 'hang'],
                'phrases': ['running slow', 'performance issues', 'system lag'],
                'weight': 0.8
            }
        }
    
    def analyze_query(self, query: str) -> QueryIntent:
        """Analyze query and extract intent, entities, and sentiment"""
        query_lower = query.lower()
        
        # Intent classification
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = 0
            
            # Check keywords
            for keyword in patterns['keywords']:
                if keyword in query_lower:
                    score += patterns['weight']
            
            # Check phrases
            for phrase in patterns['phrases']:
                if phrase in query_lower:
                    score += patterns['weight'] * 1.5
            
            intent_scores[intent] = score
        
        # Get best intent
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = min(intent_scores[best_intent] / 3.0, 1.0)  # Normalize confidence
        
        # Sentiment analysis
        blob = TextBlob(query)
        sentiment_score = blob.sentiment.polarity
        if sentiment_score > 0.1:
            sentiment = 'positive'
        elif sentiment_score < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        # Extract entities (simplified)
        entities = self._extract_entities(query)
        
        # Determine urgency
        urgency_keywords = ['urgent', 'emergency', 'critical', 'asap', 'immediately', 'now']
        urgency = 'high' if any(word in query_lower for word in urgency_keywords) else 'normal'
        
        return QueryIntent(
            intent=best_intent,
            confidence=confidence,
            entities=entities,
            sentiment=sentiment,
            urgency=urgency
        )
    
    def _extract_entities(self, query: str) -> Dict[str, Any]:
        """Extract entities from query"""
        entities = {
            'error_codes': self._extract_error_codes(query),
            'software_names': self._extract_software_names(query),
            'operating_systems': self._extract_os_names(query),
            'hardware_components': self._extract_hardware_names(query)
        }
        return entities
    
    def _extract_error_codes(self, text: str) -> List[str]:
        """Extract error codes from text"""
        patterns = [
            r'\b([A-Z][0-9]{4})\b',
            r'\b([A-Z]-[0-9]{4})\b',
            r'\b([A-Z]{2,5}[0-9]{3,5})\b',
            r'\b(0x[0-9A-Fa-f]{8})\b',
            r'\b([A-Z]{2,5}-[0-9]{3,5})\b'
        ]
        
        error_codes = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            error_codes.extend(matches)
        
        return list(set(error_codes))
    
    def _extract_software_names(self, text: str) -> List[str]:
        """Extract software names from text"""
        software_patterns = [
            'windows', 'mac', 'linux', 'chrome', 'firefox', 'safari',
            'office', 'excel', 'word', 'powerpoint', 'outlook',
            'photoshop', 'illustrator', 'zoom', 'teams', 'slack'
        ]
        
        found_software = []
        text_lower = text.lower()
        for software in software_patterns:
            if software in text_lower:
                found_software.append(software)
        
        return found_software
    
    def _extract_os_names(self, text: str) -> List[str]:
        """Extract operating system names"""
        os_patterns = ['windows', 'mac', 'macos', 'linux', 'ubuntu', 'android', 'ios']
        
        found_os = []
        text_lower = text.lower()
        for os_name in os_patterns:
            if os_name in text_lower:
                found_os.append(os_name)
        
        return found_os
    
    def _extract_hardware_names(self, text: str) -> List[str]:
        """Extract hardware component names"""
        hardware_patterns = [
            'computer', 'laptop', 'desktop', 'monitor', 'screen',
            'keyboard', 'mouse', 'printer', 'router', 'modem'
        ]
        
        found_hardware = []
        text_lower = text.lower()
        for hardware in hardware_patterns:
            if hardware in text_lower:
                found_hardware.append(hardware)
        
        return found_hardware

class KnowledgeBase:
    """Enhanced knowledge base with semantic search capabilities"""
    
    def __init__(self):
        self.solutions_db = self._initialize_solutions_database()
        self.vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
        self._build_solution_vectors()
    
    def _initialize_solutions_database(self) -> Dict[str, Any]:
        """Initialize comprehensive solutions database"""
        return {
            'technical_issues': {
                'application_crash': {
                    'issue': 'Application Crashes or Freezes',
                    'description': 'The application stops responding, crashes unexpectedly, or freezes during use.',
                    'possible_causes': [
                        'Insufficient system resources (RAM/CPU)',
                        'Software conflicts with other applications',
                        'Corrupted application files or installation',
                        'Outdated or incompatible drivers',
                        'Operating system compatibility issues',
                        'Malware or virus interference'
                    ],
                    'solution_steps': [
                        {'step': 1, 'action': 'Restart the application', 'description': 'Close the application completely and reopen it'},
                        {'step': 2, 'action': 'Update the application', 'description': 'Check for and install the latest version'},
                        {'step': 3, 'action': 'Restart your computer', 'description': 'Reboot to clear memory and refresh system resources'},
                        {'step': 4, 'action': 'Run as administrator', 'description': 'Right-click the application and select "Run as administrator"'},
                        {'step': 5, 'action': 'Check system requirements', 'description': 'Verify your system meets minimum requirements'},
                        {'step': 6, 'action': 'Reinstall the application', 'description': 'Uninstall completely and reinstall from scratch'}
                    ],
                    'prevention_tips': [
                        'Keep applications updated',
                        'Regularly restart your computer',
                        'Close unused applications to free up resources'
                    ],
                    'confidence_score': 0.95,
                    'category': 'software',
                    'severity': 'medium'
                },
                'slow_performance': {
                    'issue': 'System Running Slowly',
                    'description': 'Computer or specific applications are running slower than usual.',
                    'possible_causes': [
                        'High CPU or memory usage',
                        'Too many startup programs',
                        'Insufficient disk space',
                        'Malware or viruses',
                        'Fragmented hard drive',
                        'Background processes consuming resources'
                    ],
                    'solution_steps': [
                        {'step': 1, 'action': 'Check Task Manager', 'description': 'Open Task Manager (Ctrl+Shift+Esc) to identify resource-heavy processes'},
                        {'step': 2, 'action': 'Close unnecessary programs', 'description': 'End tasks that are using excessive CPU or memory'},
                        {'step': 3, 'action': 'Disable startup programs', 'description': 'Use Task Manager > Startup tab to disable unnecessary startup items'},
                        {'step': 4, 'action': 'Free up disk space', 'description': 'Run Disk Cleanup and delete temporary files'},
                        {'step': 5, 'action': 'Run antivirus scan', 'description': 'Perform a full system scan for malware'},
                        {'step': 6, 'action': 'Defragment hard drive', 'description': 'Use built-in defragmentation tool (for HDDs only)'}
                    ],
                    'prevention_tips': [
                        'Regularly clean temporary files',
                        'Limit startup programs',
                        'Keep antivirus updated'
                    ],
                    'confidence_score': 0.92,
                    'category': 'performance',
                    'severity': 'low'
                },
                'network_issues': {
                    'issue': 'Internet Connection Problems',
                    'description': 'Unable to connect to the internet or experiencing slow/intermittent connectivity.',
                    'possible_causes': [
                        'Router or modem issues',
                        'ISP service problems',
                        'DNS server issues',
                        'Network adapter driver problems',
                        'Firewall or antivirus blocking connection',
                        'IP address conflicts'
                    ],
                    'solution_steps': [
                        {'step': 1, 'action': 'Check physical connections', 'description': 'Ensure all cables are securely connected'},
                        {'step': 2, 'action': 'Restart network devices', 'description': 'Unplug router/modem for 30 seconds, then plug back in'},
                        {'step': 3, 'action': 'Run network troubleshooter', 'description': 'Use Windows Network Troubleshooter'},
                        {'step': 4, 'action': 'Flush DNS cache', 'description': 'Open Command Prompt as admin and run "ipconfig /flushdns"'},
                        {'step': 5, 'action': 'Update network drivers', 'description': 'Update network adapter drivers through Device Manager'},
                        {'step': 6, 'action': 'Reset network settings', 'description': 'Use "netsh winsock reset" and "netsh int ip reset" commands'}
                    ],
                    'prevention_tips': [
                        'Keep router firmware updated',
                        'Position router in central location',
                        'Regularly restart network equipment'
                    ],
                    'confidence_score': 0.90,
                    'category': 'network',
                    'severity': 'medium'
                },
                'login_problems': {
                    'issue': 'Cannot Log In or Authentication Failed',
                    'description': 'Unable to sign in to applications, websites, or system accounts.',
                    'possible_causes': [
                        'Incorrect username or password',
                        'Account locked due to multiple failed attempts',
                        'Expired or changed credentials',
                        'Two-factor authentication issues',
                        'Browser cache and cookies problems',
                        'Account security restrictions'
                    ],
                    'solution_steps': [
                        {'step': 1, 'action': 'Verify credentials', 'description': 'Double-check username and password for typos'},
                        {'step': 2, 'action': 'Clear browser data', 'description': 'Clear cookies, cache, and saved passwords'},
                        {'step': 3, 'action': 'Try incognito/private mode', 'description': 'Test login in a private browsing window'},
                        {'step': 4, 'action': 'Reset password', 'description': 'Use the "Forgot Password" option to reset credentials'},
                        {'step': 5, 'action': 'Check account status', 'description': 'Contact administrator to verify account is active'},
                        {'step': 6, 'action': 'Try different browser', 'description': 'Test with an alternative web browser'}
                    ],
                    'prevention_tips': [
                        'Use strong, unique passwords',
                        'Enable two-factor authentication',
                        'Keep recovery information updated'
                    ],
                    'confidence_score': 0.88,
                    'category': 'authentication',
                    'severity': 'medium'
                },
                'file_corruption': {
                    'issue': 'File Corruption or Cannot Open Files',
                    'description': 'Files are corrupted, cannot be opened, or display error messages.',
                    'possible_causes': [
                        'Improper system shutdown',
                        'Storage device failures',
                        'Virus or malware infection',
                        'Software bugs or conflicts',
                        'Network interruptions during file transfer',
                        'Physical damage to storage media'
                    ],
                    'solution_steps': [
                        {'step': 1, 'action': 'Try different application', 'description': 'Open the file with an alternative program'},
                        {'step': 2, 'action': 'Restore from backup', 'description': 'Use a backup copy if available'},
                        {'step': 3, 'action': 'Run file repair tools', 'description': 'Use built-in repair utilities for specific file types'},
                        {'step': 4, 'action': 'Check disk for errors', 'description': 'Run CHKDSK to scan for and fix disk errors'},
                        {'step': 5, 'action': 'Use data recovery software', 'description': 'Try specialized recovery tools for important files'},
                        {'step': 6, 'action': 'Restore system to earlier point', 'description': 'Use System Restore to roll back to when files worked'}
                    ],
                    'prevention_tips': [
                        'Regular backups of important files',
                        'Proper system shutdown procedures',
                        'Keep antivirus software updated'
                    ],
                    'confidence_score': 0.85,
                    'category': 'files',
                    'severity': 'high'
                }
            },
            'how_to_guides': {
                'software_installation': {
                    'issue': 'How to Install Software Safely',
                    'description': 'Step-by-step guide for installing new software applications.',
                    'solution_steps': [
                        {'step': 1, 'action': 'Download from official source', 'description': 'Always download software from the official website or trusted sources'},
                        {'step': 2, 'action': 'Verify system requirements', 'description': 'Check that your system meets minimum requirements'},
                        {'step': 3, 'action': 'Run antivirus scan', 'description': 'Scan the downloaded file before installation'},
                        {'step': 4, 'action': 'Create system restore point', 'description': 'Create a restore point in case you need to roll back'},
                        {'step': 5, 'action': 'Run as administrator', 'description': 'Right-click installer and select "Run as administrator"'},
                        {'step': 6, 'action': 'Follow installation wizard', 'description': 'Complete the installation following on-screen instructions'}
                    ],
                    'confidence_score': 0.95,
                    'category': 'tutorial'
                },
                'password_security': {
                    'issue': 'How to Create Strong Passwords',
                    'description': 'Guidelines for creating and managing secure passwords.',
                    'solution_steps': [
                        {'step': 1, 'action': 'Use minimum 12 characters', 'description': 'Create passwords with at least 12 characters'},
                        {'step': 2, 'action': 'Mix character types', 'description': 'Include uppercase, lowercase, numbers, and symbols'},
                        {'step': 3, 'action': 'Avoid personal information', 'description': 'Don\'t use names, birthdays, or other personal data'},
                        {'step': 4, 'action': 'Use unique passwords', 'description': 'Create different passwords for each account'},
                        {'step': 5, 'action': 'Consider passphrases', 'description': 'Use memorable phrases with character substitutions'},
                        {'step': 6, 'action': 'Use password manager', 'description': 'Employ a reputable password management tool'}
                    ],
                    'confidence_score': 0.98,
                    'category': 'security'
                }
            }
        }
    
    def _build_solution_vectors(self):
        """Build TF-IDF vectors for semantic search"""
        all_solutions = []
        self.solution_keys = []
        
        for category, solutions in self.solutions_db.items():
            for key, solution in solutions.items():
                text = f"{solution['issue']} {solution['description']} " + \
                       " ".join(solution.get('possible_causes', []))
                all_solutions.append(text)
                self.solution_keys.append((category, key))
        
        if all_solutions:
            self.solution_vectors = self.vectorizer.fit_transform(all_solutions)
    
    def find_solution(self, query: str, intent: QueryIntent) -> Dict[str, Any]:
        """Find best matching solution using semantic search"""
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.solution_vectors)[0]
        
        # Get best matches
        best_indices = np.argsort(similarities)[::-1][:3]
        best_solutions = []
        
        for idx in best_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                category, key = self.solution_keys[idx]
                solution = self.solutions_db[category][key].copy()
                solution['similarity_score'] = float(similarities[idx])
                best_solutions.append(solution)
        
        if best_solutions:
            return best_solutions[0]
        
        # Fallback to intent-based matching
        return self._fallback_solution(intent)
    
    def _fallback_solution(self, intent: QueryIntent) -> Dict[str, Any]:
        """Provide fallback solution based on intent"""
        fallback_solutions = {
            'technical_issue': {
                'issue': 'General Technical Issue',
                'description': 'A general technical problem that needs troubleshooting.',
                'solution_steps': [
                    {'step': 1, 'action': 'Identify the problem', 'description': 'Clearly describe what is not working'},
                    {'step': 2, 'action': 'Check for error messages', 'description': 'Note any error codes or messages'},
                    {'step': 3, 'action': 'Restart the application/system', 'description': 'Try a simple restart first'},
                    {'step': 4, 'action': 'Check for updates', 'description': 'Update software and drivers'},
                    {'step': 5, 'action': 'Search for specific solutions', 'description': 'Look up error codes or specific symptoms'}
                ],
                'confidence_score': 0.6
            },
            'how_to': {
                'issue': 'How-to Request',
                'description': 'Request for instructions or guidance.',
                'solution_steps': [
                    {'step': 1, 'action': 'Research the topic', 'description': 'Look up official documentation or tutorials'},
                    {'step': 2, 'action': 'Follow step-by-step guides', 'description': 'Use reputable sources for instructions'},
                    {'step': 3, 'action': 'Practice safely', 'description': 'Test in a safe environment first'},
                    {'step': 4, 'action': 'Ask for help if needed', 'description': 'Contact support or community forums'}
                ],
                'confidence_score': 0.5
            }
        }
        
        return fallback_solutions.get(intent.intent, fallback_solutions['technical_issue'])

class VirtualAssistantService:
    """
    Advanced Virtual Assistant Service with NLP and Brain System Integration
    """
    
    def __init__(self):
        self.nlp_processor = NLPProcessor()
        self.knowledge_base = KnowledgeBase()
        self.conversation_history = {}
        self.session_data = {}
        
        # Import brain core for integration
        try:
            from .brain_core import BrainCore
            self.brain_core = BrainCore()
        except ImportError:
            logger.warning("Brain core not available, using local processing only")
            self.brain_core = None
        
        try:
            from .huggingface_service import HuggingFaceService
            self.hf_service = HuggingFaceService()
        except ImportError:
            logger.warning("Hugging Face service not available")
            self.hf_service = None
        
    async def process_chat_message(self, user_input: str, session_id: str = None, 
                                 user_id: str = "default_user") -> Dict[str, Any]:
        """
        Process a chat message and generate intelligent response
        
        Args:
            user_input: The user's message
            session_id: Session identifier
            user_id: User identifier
            
        Returns:
            Dict with response data
        """
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Initialize session
        self._initialize_session(session_id, user_id)
        
        # Analyze query with NLP
        intent = self.nlp_processor.analyze_query(user_input)
        
        # Try brain system first if available
        brain_result = None
        if self.brain_core:
            try:
                brain_result = await self._process_with_brain(user_input, user_id)
            except Exception as e:
                logger.error(f"Brain system error: {e}")
        
        # Use local knowledge base if brain system fails or has low confidence
        if not brain_result or brain_result.get('confidence_score', 0) < 0.7:
            solution = self.knowledge_base.find_solution(user_input, intent)
        else:
            solution = brain_result
        
        # Generate response
        response_text = self._generate_response_text(user_input, intent, solution)
        
        # Generate follow-up questions
        follow_up_questions = self._generate_follow_up_questions(intent, solution)
        
        # Generate suggested actions
        suggested_actions = self._generate_suggested_actions(intent, solution)
        
        # Create response
        query_id = str(uuid.uuid4())
        response = {
            "query_id": query_id,
            "session_id": session_id,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "solution": {
                "issue": solution.get('issue', 'General Assistance'),
                "possible_causes": solution.get('possible_causes', []),
                "recommended_steps": [
                    {
                        "step_number": step.get('step', i + 1),
                        "description": f"{step.get('action', 'Step')}: {step.get('description', '')}"
                    }
                    for i, step in enumerate(solution.get('solution_steps', []))
                ],
                "confidence_score": solution.get('confidence_score', 0.5)
            },
            "follow_up_questions": follow_up_questions,
            "suggested_actions": suggested_actions,
            "metadata": {
                'intent': intent.intent,
                'intent_confidence': intent.confidence,
                'sentiment': intent.sentiment,
                'urgency': intent.urgency,
                'entities': intent.entities,
                'solution_category': solution.get('category', 'general'),
                'timestamp': datetime.now().isoformat()
            }
        }
        
        # Store in session
        self._update_session(session_id, user_input, response)
        
        return {
            "success": True,
            "result": response
        }
    
    async def _process_with_brain(self, query: str, user_id: str) -> Dict[str, Any]:
        """Process query using the brain core system"""
        try:
            input_data = {
                "input_type": "text",
                "text_query": query,
                "user_id": user_id
            }
            
            brain_result = await self.brain_core.process_input(input_data)
            return brain_result.get("solution", {})
            
        except Exception as e:
            logger.error(f"Error processing with brain system: {e}")
            return None
    
    def _initialize_session(self, session_id: str, user_id: str):
        """Initialize session data"""
        if session_id not in self.session_data:
            self.session_data[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now(),
                'messages': [],
                'context': {},
                'interaction_count': 0
            }
    
    def _update_session(self, session_id: str, query: str, response: Dict[str, Any]):
        """Update session with new interaction"""
        session = self.session_data[session_id]
        session['messages'].append({
            'query': query,
            'response': response,
            'timestamp': datetime.now()
        })
        session['interaction_count'] += 1
        session['context']['last_intent'] = response['metadata']['intent']
        session['context']['last_category'] = response['metadata']['solution_category']
    
    def _generate_response_text(self, query: str, intent: QueryIntent, solution: Dict[str, Any]) -> str:
        """Generate natural language response text"""
        
        # Greeting based on sentiment and urgency
        if intent.urgency == 'high':
            greeting = "I understand this is urgent. Let me help you resolve this quickly."
        elif intent.sentiment == 'negative':
            greeting = "I can see you're experiencing some difficulties. I'm here to help."
        else:
            greeting = "I'd be happy to help you with this issue."
        
        # Problem acknowledgment
        problem_ack = f"It looks like you're dealing with: **{solution['issue']}**"
        
        # Description
        description = solution.get('description', '')
        
        # Confidence indicator
        confidence = solution.get('confidence_score', 0.5)
        if confidence > 0.8:
            confidence_text = "I'm confident this solution will help resolve your issue."
        elif confidence > 0.6:
            confidence_text = "This solution should help address your problem."
        else:
            confidence_text = "Here's a general approach that may help with your situation."
        
        # Combine response
        response_parts = [greeting, problem_ack]
        
        if description:
            response_parts.append(description)
        
        response_parts.append(confidence_text)
        
        if solution.get('possible_causes'):
            response_parts.append("\n**Possible causes include:**")
            for cause in solution['possible_causes'][:3]:  # Limit to top 3
                response_parts.append(f"• {cause}")
        
        response_parts.append("\nI've provided detailed steps below to help resolve this issue.")
        
        return "\n\n".join(response_parts)
    
    def _generate_follow_up_questions(self, intent: QueryIntent, solution: Dict[str, Any]) -> List[str]:
        """Generate contextual follow-up questions"""
        questions = []
        
        # Intent-based questions
        if intent.intent == 'technical_issue':
            questions.extend([
                "Are you seeing any specific error messages?",
                "When did this problem first start occurring?",
                "Have you made any recent changes to your system?",
                "Is this happening on multiple devices or just one?"
            ])
        elif intent.intent == 'performance':
            questions.extend([
                "How long has the system been running slowly?",
                "Does this happen with all applications or specific ones?",
                "Have you noticed high CPU or memory usage?",
                "When was the last time you restarted your computer?"
            ])
        elif intent.intent == 'network':
            questions.extend([
                "Are other devices on the network working properly?",
                "Have you tried restarting your router?",
                "Are you using WiFi or ethernet connection?",
                "Has your internet service provider reported any outages?"
            ])
        
        # General troubleshooting questions
        if len(questions) < 3:
            questions.extend([
                "Have you tried restarting the application or device?",
                "Are you able to reproduce this problem consistently?",
                "Would you like me to explain any of the solution steps in more detail?"
            ])
        
        return questions[:4]  # Limit to 4 questions
    
    def _generate_suggested_actions(self, intent: QueryIntent, solution: Dict[str, Any]) -> List[str]:
        """Generate suggested quick actions"""
        actions = []
        
        # Based on solution category
        category = solution.get('category', 'general')
        
        if category == 'software':
            actions.extend([
                "Check for software updates",
                "Run the application as administrator",
                "Restart your computer"
            ])
        elif category == 'network':
            actions.extend([
                "Restart your router and modem",
                "Run Windows Network Troubleshooter",
                "Check network cable connections"
            ])
        elif category == 'performance':
            actions.extend([
                "Open Task Manager to check resource usage",
                "Close unnecessary applications",
                "Run Disk Cleanup"
            ])
        elif category == 'security':
            actions.extend([
                "Run a full antivirus scan",
                "Check Windows Security settings",
                "Update your passwords"
            ])
        
        # Default actions if none specified
        if not actions:
            actions.extend([
                "Restart the affected application",
                "Check for system updates",
                "Review any recent changes made to your system"
            ])
        
        return actions[:3]  # Limit to 3 actions
    
    async def process_voice_query(self, audio_data: bytes, user_id: str, session_id: str = None) -> Dict[str, Any]:
        """Process voice query using speech-to-text and then process as text"""
        try:
            if not self.hf_service:
                return {
                    "success": False,
                    "error": "Speech-to-text service not available"
                }
            
            # Convert speech to text using Hugging Face
            transcribed_text = await self.hf_service.transcribe_audio(audio_data)
            
            if not transcribed_text or transcribed_text.strip() == "":
                transcribed_text = "I'm having a technical issue with my device"
            
            # Process the transcribed text
            return await self.process_chat_message(transcribed_text, session_id, user_id)
            
        except Exception as e:
            logger.error(f"Error processing voice query: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_quick_actions(self) -> Dict[str, Any]:
        """Get available quick actions for the virtual assistant"""
        return {
            "system_diagnostics": {
                "title": "System Diagnostics",
                "description": "Run comprehensive system health check",
                "steps": [
                    {"step_number": 1, "description": "Check system resources (CPU, RAM, Disk)"},
                    {"step_number": 2, "description": "Scan for malware and viruses"},
                    {"step_number": 3, "description": "Check for Windows updates"},
                    {"step_number": 4, "description": "Run disk cleanup and optimization"},
                    {"step_number": 5, "description": "Generate system health report"}
                ]
            },
            "network_troubleshooting": {
                "title": "Network Troubleshooting",
                "description": "Diagnose and fix network connectivity issues",
                "steps": [
                    {"step_number": 1, "description": "Test internet connectivity"},
                    {"step_number": 2, "description": "Check network adapter status"},
                    {"step_number": 3, "description": "Reset network settings"},
                    {"step_number": 4, "description": "Flush DNS cache"},
                    {"step_number": 5, "description": "Contact ISP if issues persist"}
                ]
            },
            "performance_optimization": {
                "title": "Performance Optimization",
                "description": "Optimize system performance and speed",
                "steps": [
                    {"step_number": 1, "description": "Disable unnecessary startup programs"},
                    {"step_number": 2, "description": "Clean temporary files and cache"},
                    {"step_number": 3, "description": "Defragment hard drive"},
                    {"step_number": 4, "description": "Update device drivers"},
                    {"step_number": 5, "description": "Consider hardware upgrades"}
                ]
            }
        }
    
    def get_session_history(self, session_id: str) -> Dict[str, Any]:
        """Get conversation history for a specific session"""
        if session_id in self.session_data:
            session = self.session_data[session_id]
            return {
                "success": True,
                "session": {
                    'session_id': session_id,
                    'user_id': session['user_id'],
                    'created_at': session['created_at'].isoformat(),
                    'interaction_count': session['interaction_count'],
                    'messages': [
                        {
                            'query': msg['query'],
                            'response_text': msg['response']['solution']['issue'],
                            'confidence_score': msg['response']['solution']['confidence_score'],
                            'timestamp': msg['timestamp'].isoformat()
                        }
                        for msg in session['messages']
                    ],
                    'context': session['context']
                }
            }
        else:
            return {
                "success": False,
                "error": "Session not found"
            }
    
    def get_all_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all sessions for a specific user"""
        user_sessions = []
        for session_id, session_data in self.session_data.items():
            if session_data["user_id"] == user_id:
                user_sessions.append({
                    "session_id": session_id,
                    "created_at": session_data["created_at"].isoformat(),
                    "interaction_count": session_data["interaction_count"],
                    "last_query": session_data["context"].get("last_query", ""),
                    "last_issue": session_data["context"].get("last_issue", "")
                })
        
        return sorted(user_sessions, key=lambda x: x["created_at"], reverse=True)
    
    def _cleanup_sessions(self):
        """Clean up old sessions to prevent memory issues"""
        if len(self.session_data) > 100:
            # Remove oldest sessions beyond the limit
            sorted_sessions = sorted(
                self.session_data.items(), 
                key=lambda x: x[1]["created_at"]
            )
            for session_id, _ in sorted_sessions[:-100]:
                del self.session_data[session_id]
    
    def get_assistant_stats(self) -> Dict[str, Any]:
        """Get virtual assistant statistics"""
        total_sessions = len(self.session_data)
        total_interactions = sum(session["interaction_count"] for session in self.session_data.values())
        
        # Intent distribution
        intent_counts = {}
        for session in self.session_data.values():
            for message in session["messages"]:
                intent = message["response"]["metadata"].get("intent", "unknown")
                intent_counts[intent] = intent_counts.get(intent, 0) + 1
        
        return {
            "total_sessions": total_sessions,
            "total_interactions": total_interactions,
            "active_sessions": len([s for s in self.session_data.values() if s["interaction_count"] > 0]),
            "knowledge_base_size": len(self.knowledge_base.solutions_db["technical_issues"]) + len(self.knowledge_base.solutions_db["how_to_guides"]),
            "intent_distribution": intent_counts,
            "uptime": datetime.now().isoformat()
        }
