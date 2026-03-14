import React, { useState } from "react";
import { Box, Typography, Avatar, IconButton, TextField, Paper, Drawer, Divider } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';

export default function ChatConversation({ contact, messages, onSendMessage, onBack }) {
  const [input, setInput] = useState("");
  const [showProfile, setShowProfile] = useState(false);

  // Consolidated sending logic to ensure the box clears
  const handleAction = () => {
    if (!input.trim()) return;
    onSendMessage(contact.id, input);
    setInput(""); // <--- This clears the text box
  };

  return (
    <Box sx={{ height: '100%', display: 'flex' }}>
      <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
        
        {/* HEADER */}
        <Box sx={{ p: 2, display: 'flex', alignItems: 'center', borderBottom: '1px solid', borderColor: 'divider', bgcolor: 'background.paper' }}>
          <Avatar 
            sx={{ bgcolor: 'primary.main', mr: 2, cursor: 'pointer', color: 'background.default' }} 
            onClick={() => setShowProfile(true)}
          >
            {contact.name[0]}
          </Avatar>
          <Box sx={{ flexGrow: 1, cursor: 'pointer' }} onClick={() => setShowProfile(true)}>
            <Typography variant="subtitle1" sx={{ fontWeight: 700, lineHeight: 1.2 }}>{contact.name}</Typography>
            <Typography variant="caption" sx={{ color: 'primary.main' }}>View Profile</Typography>
          </Box>
          <IconButton onClick={() => setShowProfile(true)}><InfoOutlinedIcon /></IconButton>
        </Box>

        {/* FEED */}
        <Box sx={{ flexGrow: 1, p: 3, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 2 }}>
          {messages.map((msg) => (
            <Box key={msg.id} sx={{ alignSelf: msg.sender === "me" ? "flex-end" : "flex-start", maxWidth: "70%" }}>
              <Paper sx={{ 
                p: 2, 
                borderRadius: 3, 
                bgcolor: msg.sender === "me" ? "primary.main" : "background.paper", 
                color: msg.sender === "me" ? "background.default" : "text.primary", 
                border: msg.sender === "me" ? "none" : "1px solid", 
                borderColor: "divider",
                boxShadow: msg.sender === "me" ? 4 : 0
              }}>
                <Typography variant="body2" sx={{ fontSize: '0.95rem' }}>{msg.text}</Typography>
              </Paper>
              
              {/* TIME RENDERING */}
              <Typography 
                variant="caption" 
                sx={{ 
                  mt: 0.5, 
                  display: 'block', 
                  textAlign: msg.sender === "me" ? "right" : "left", 
                  opacity: 0.5,
                  fontSize: '0.7rem'
                }}
              >
                {msg.time}
              </Typography>
            </Box>
          ))}
        </Box>

        {/* INPUT AREA */}
        <Box sx={{ p: 2, borderTop: '1px solid', borderColor: 'divider', bgcolor: 'background.paper' }}>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField 
              fullWidth 
              placeholder="Message..." 
              value={input} 
              onChange={(e) => setInput(e.target.value)} 
              onKeyPress={(e) => e.key === 'Enter' && handleAction()} // Added clearing here too
              sx={{ 
                '& .MuiOutlinedInput-root': { 
                    borderRadius: 6, 
                    bgcolor: 'background.default',
                    border: '1px solid',
                    borderColor: 'divider'
                } 
              }} 
            />
            <IconButton 
              onClick={handleAction} 
              sx={{ 
                bgcolor: 'primary.main', 
                color: 'background.default',
                '&:hover': { bgcolor: 'primary.dark' }
              }}
            >
              <SendIcon />
            </IconButton>
          </Box>
        </Box>
      </Box>

      {/* PROFILE SIDE DRAWER (Remains same as previous implementation) */}
      <Drawer anchor="right" open={showProfile} onClose={() => setShowProfile(false)}>
        <Box sx={{ width: 350, bgcolor: 'background.paper', height: '100%', p: 4, color: 'text.primary' }}>
          {/* ... Profile Content ... */}
          <Box textAlign="center" mb={4}>
            <Avatar sx={{ width: 100, height: 100, fontSize: '2rem', mx: 'auto', mb: 2, bgcolor: 'primary.main', color: 'background.default' }}>{contact.name[0]}</Avatar>
            <Typography variant="h3" sx={{ fontFamily: 'Playfair Display', fontSize: '1.8rem' }}>{contact.name}</Typography>
            <Typography color="primary.main" fontWeight="700">{contact.role}</Typography>
          </Box>
          <Divider sx={{ mb: 3 }} />
          <Typography variant="subtitle2" color="text.secondary" gutterBottom>DEPARTMENT</Typography>
          <Typography variant="body1" sx={{ mb: 3 }}>{contact.dept}</Typography>
          <Typography variant="subtitle2" color="text.secondary" gutterBottom>ABOUT</Typography>
          <Typography variant="body1" sx={{ mb: 3 }}>{contact.bio}</Typography>
        </Box>
      </Drawer>
    </Box>
  );
}