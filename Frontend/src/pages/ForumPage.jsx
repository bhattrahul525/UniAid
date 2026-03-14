import { useState } from "react";
import { Box, Typography, Fab, useTheme } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import ForumPost from "./ForumPost";
import ThreadView from "./ThreadView";
import CreatePostView from "./CreatePostView"; // We'll create this next

export default function ForumPage() {
  const [selectedPost, setSelectedPost] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const theme = useTheme();

  const [posts, setPosts] = useState([
    { id: 1, title: "Adjusting to the new academic year", author: "Emily Rodriguez (Alumni)", description: " Here are some handy tips to ensure you are ready for the upocming semester. Make sure to eat and sleep well. Join the clubs and activities that interest you, and have a healthy work-life balance.", category: "Advice", timestamp: "10:30 AM" },
    { id: 2, title: "Campus Student Support services", author: "Michael Chen (Parent)", description: "Hello everyone, I was wondering what services are available on campus for student welfare, in terms of security, medical checkups, and mental health support, and how useful these truly are.", category: "Discussion", timestamp: "Yesterday" },
    { id: 3, title: "Information Technology department workload", author: "Sarah Mitchell (Student)", description: "I recently joined the Information Technology department, and I was wondering how stressful the workload is, and how much time I should allocate to it.", category: "Mentoring", timestamp: "Monday" }
  ]);

  const handleCreatePost = (newPost) => {
    const postWithId = { ...newPost, id: Date.now(), timestamp: "Just now" };
    setPosts([postWithId, ...posts]);
    setSelectedPost(postWithId);
    setIsCreating(false);
  };

  return (
    <Box sx={{ backgroundColor: "background.default", height: "100vh", display: "flex", overflow: "hidden",        height: "calc(100vh - 160px)", }}>
      
      {/* LEFT SIDEBAR */}
      <Box sx={{ 
        width: { xs: "100%", md: "400px" }, 
        borderRight: "1px solid", 
        borderColor: "divider",
        bgcolor: "background.paper",
        overflowY: "auto",
        display: (selectedPost || isCreating) && { xs: "none", md: "block" }
      }}>        
        {posts.map((post) => (
          <ForumPost 
            key={post.id} 
            {...post} 
            isSelected={selectedPost?.id === post.id}
            onClick={() => {
                setSelectedPost(post);
                setIsCreating(false); // Close create mode if user clicks a post
            }} 
          />
        ))}
      </Box>

      {/* RIGHT SIDE: Dynamic View */}
      <Box sx={{ flexGrow: 1, overflowY: "auto", height: "100%" }}>
        {isCreating ? (
          <Box sx={{ width: "100%", maxWidth: '800px', mx: 'auto', p: { xs: 2, md: 6 } }}>
            <CreatePostView 
              onCancel={() => setIsCreating(false)} 
              onSubmit={handleCreatePost} 
            />
          </Box>
        ) : selectedPost ? (
          <Box sx={{ width: "100%", maxWidth: '900px', mx: 'auto', p: { xs: 2, md: 6 } }}>
            <ThreadView 
              key={selectedPost.id} 
              post={selectedPost} 
              onBack={() => setSelectedPost(null)} 
            />
          </Box>
        ) : (
          <Box sx={{ height: "100%", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <Typography color="text.secondary" variant="h5" sx={{ fontFamily: 'Playfair Display', opacity: 0.5 }}>
              Select a thread or create a new one
            </Typography>
          </Box>
        )}
      </Box>

      {/* FAB: Only show if not already creating */}
      {!isCreating && (
        <Fab 
          color="primary" 
          onClick={() => setIsCreating(true)}
          sx={{ position: "fixed", bottom: 40, right: 40 }}
        >
          <AddIcon sx={{ color: "background.default" }} />
        </Fab>
      )}
    </Box>
  );
}