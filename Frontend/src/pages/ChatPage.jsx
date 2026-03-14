import React, { useState } from "react";
import {
  Box,
  Typography,
  Avatar,
  Autocomplete,
  TextField,
  InputAdornment,
  Badge
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import ChatConversation from "./ChatConversation";

// Global database of people
const allUsers = [
  {
    id: 1,
    name: "Dr. Emily Rodriguez",
    role: "Senior Lecturer",
    dept: "Computer Science",
    bio: "Researching Neural Networks since 2015."
  },
  {
    id: 2,
    name: "Michael Chen",
    role: "Student",
    dept: "Software Engineering",
    bio: "React enthusiast and Coffee addict."
  },
  {
    id: 3,
    name: "Sarah Mitchell",
    role: "Tutor",
    dept: "Mathematics",
    bio: "Here to help with any DSA questions!"
  },
  { id: 4, name: "Professor Snape", role: "Faculty", dept: "Chemistry", bio: "Turn to page 394." }
];

export default function ChatPage() {
  const [selectedContact, setSelectedContact] = useState(null);
  const [conversations, setConversations] = useState({});

  // Filter history: Users who have messages
  const chatHistory = allUsers.filter((user) => conversations[user.id]);

  const startChat = (user) => {
    if (!user) return;
    if (!conversations[user.id]) {
      setConversations((prev) => ({ ...prev, [user.id]: [] }));
    }
    setSelectedContact(user);
  };

  const handleSendMessage = (contactId, text) => {
    const newMessage = {
      id: Date.now(),
      text,
      sender: "me",
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    };
    setConversations((prev) => ({
      ...prev,
      [contactId]: [...(prev[contactId] || []), newMessage]
    }));
  };

  return (
    <Box
      sx={{
        backgroundColor: "background.default",
        height: "calc(100vh - 160px)",
        display: "flex",
        overflow: "hidden"
      }}
    >
      {/* SIDEBAR */}
      <Box
        sx={{
          width: { xs: "100%", md: "380px" },
          borderRight: "1px solid",
          borderColor: "divider",
          bgcolor: "background.paper",
          display: selectedContact && { xs: "none", md: "flex" },
          flexDirection: "column"
        }}
      >
        <Box sx={{ p: 3 }}>
          {/* SEARCHABLE DROPDOWN (Autocomplete) */}
          <Autocomplete
            options={allUsers}
            getOptionLabel={(option) => option.name}
            onChange={(event, newValue) => startChat(newValue)}
            // Style the dropdown list
            slotProps={{
              paper: {
                sx: {
                  mt: 1,
                  borderRadius: 3,
                  boxShadow: "0 10px 25px rgba(0,0,0,0.1)"
                }
              }
            }}
            renderInput={(params) => (
              <TextField
                {...params}
                placeholder="Search people..."
                variant="outlined"
                fullWidth
                sx={{
                  background: "#ffffff",
                  borderRadius: "40px",

                  "& .MuiOutlinedInput-root": {
                    borderRadius: "40px",
                    transition: "all 0.25s ease",
                    boxShadow: "0 4px 12px rgba(0,0,0,0.08)",

                    "& fieldset": {
                      borderColor: "rgba(0,0,0,0.08)"
                    },

                    "&:hover fieldset": {
                      borderColor: "#1976d2"
                    },

                    "&.Mui-focused fieldset": {
                      borderColor: "#1976d2",
                      borderWidth: "2px"
                    },

                    "&.Mui-focused": {
                      boxShadow: "0 6px 20px rgba(25,118,210,0.25)"
                    }
                  },

                  "& input": {
                    padding: "14px 10px",
                    fontSize: "15px"
                  }
                }}
                InputProps={{
                  ...params.InputProps,
                  startAdornment: (
                    <>
                      <InputAdornment position="start">
                        <SearchIcon sx={{ color: "text.secondary" }} />
                      </InputAdornment>
                      {params.InputProps.startAdornment}
                    </>
                  )
                }}
              />
            )}
            // Style each individual option in the dropdown
            renderOption={(props, option) => (
              <Box component="li" {...props} sx={{ display: "flex", gap: 2, p: 1.5 }}>
                <Avatar sx={{ bgcolor: "primary.main", width: 32, height: 32, fontSize: "0.8rem" }}>
                  {option.name[0]}
                </Avatar>
                <Box>
                  <Typography variant="body2" sx={{ fontWeight: 700 }}>
                    {option.name}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {option.role}
                  </Typography>
                </Box>
              </Box>
            )}
          />
        </Box>

        {/* CHAT HISTORY LIST */}
        <Box sx={{ flexGrow: 1, overflowY: "auto" }}>
          <Typography
            variant="caption"
            sx={{
              px: 3,
              py: 1,
              display: "block",
              color: "text.secondary",
              fontWeight: 700,
              letterSpacing: 1
            }}
          >
            RECENT CHATS
          </Typography>
          {chatHistory.length > 0 ? (
            chatHistory.map((user) => (
              <Box
                key={user.id}
                onClick={() => setSelectedContact(user)}
                sx={{
                  p: 2.5,
                  display: "flex",
                  alignItems: "center",
                  cursor: "pointer",
                  bgcolor:
                    selectedContact?.id === user.id ? "rgba(143, 167, 140, 0.08)" : "transparent",
                  borderLeft: "4px solid",
                  borderColor: selectedContact?.id === user.id ? "primary.main" : "transparent",
                  "&:hover": { bgcolor: "rgba(255, 255, 255, 0.03)" }
                }}
              >
                <Avatar sx={{ bgcolor: "primary.dark", mr: 2 }}>{user.name[0]}</Avatar>
                <Box sx={{ flexGrow: 1 }}>
                  <Typography variant="body1" sx={{ fontWeight: 700 }}>
                    {user.name}
                  </Typography>
                  <Typography
                    variant="body2"
                    color="text.secondary"
                    noWrap
                    sx={{ fontSize: "0.85rem" }}
                  >
                    {conversations[user.id]?.slice(-1)[0]?.text || "New conversation started"}
                  </Typography>
                </Box>
              </Box>
            ))
          ) : (
            <Box sx={{ p: 6, textAlign: "center", opacity: 0.4 }}>
              <Typography variant="body2">Your inbox is empty.</Typography>
              <Typography variant="caption">Search for a colleague to begin.</Typography>
            </Box>
          )}
        </Box>
      </Box>

      {/* CHAT VIEW (Uses previous fixed logic) */}
      <Box sx={{ flexGrow: 1 }}>
        {selectedContact ? (
          <ChatConversation
            key={selectedContact.id}
            contact={selectedContact}
            messages={conversations[selectedContact.id] || []}
            onSendMessage={handleSendMessage}
            onBack={() => setSelectedContact(null)}
          />
        ) : (
          <Box
            sx={{
              height: "100%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              opacity: 0.3
            }}
          >
            <Box textAlign="center">
              <Typography variant="h3" sx={{ fontFamily: "Playfair Display", mb: 1 }}>
                UniAid Connect
              </Typography>
              <Typography variant="body1">Select a conversation to view messages</Typography>
            </Box>
          </Box>
        )}
      </Box>
    </Box>
  );
}
