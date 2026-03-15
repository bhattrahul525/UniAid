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
  {
    id: 1,
    title: "Affordable places to eat near UniMelb?",
    author: "Rahul Sharma (New Student)",
    description:
      "Hi everyone! I just moved to Melbourne and I'm trying to save money on food. Does anyone know affordable places to eat near the University of Melbourne?",
    category: "Food",
    timestamp: "Today",
    comments: [
      {
        id: 101,
        author: "Jessica Lee (Student)",
        text:
          "You should try these places:\n\n1. Guzman y Gomez – great burritos and bowls for around $10.\n2. Don Tojo – really popular Japanese place near campus.\n3. Universal Restaurant – famous for cheap student pasta deals."
      },
      {
        id: 102,
        author: "Daniel Wong (Student)",
        text:
          "Universal Restaurant is amazing for students. Big pasta plates for around $10–12."
      }
    ]
  },

  {
    id: 2,
    title: "Best coffee near University of Melbourne?",
    author: "Lucas Martin (Exchange Student)",
    description:
      "Everyone says Melbourne has the best coffee culture in the world. Any café recommendations near campus?",
    category: "Food",
    timestamp: "Today",
    comments: [
      {
        id: 201,
        author: "Emma Chen (Student)",
        text:
          "Code Black Coffee is very popular with students and locals."
      },
      {
        id: 202,
        author: "Oliver Grant (Student)",
        text:
          "Seven Seeds is another famous café close to campus. Definitely worth visiting."
      }
    ]
  },

  {
    id: 3,
    title: "Where do students buy cheap groceries?",
    author: "Ahmed Khan (New Student)",
    description:
      "I'm trying to cook more instead of eating outside. Which supermarkets are cheapest for students in Melbourne?",
    category: "Living",
    timestamp: "Yesterday",
    comments: [
      {
        id: 301,
        author: "Sophie Taylor (Student)",
        text:
          "Aldi is usually the cheapest supermarket in Australia."
      },
      {
        id: 302,
        author: "Ryan Patel (Student)",
        text:
          "Coles and Woolworths are everywhere but Aldi is best if you're on a student budget."
      }
    ]
  },

  {
    id: 4,
    title: "Late night food options near campus?",
    author: "Emily Zhang (Student)",
    description:
      "Sometimes we study late in the library and everything seems closed. Where can we get food late at night?",
    category: "Food",
    timestamp: "Yesterday",
    comments: [
      {
        id: 401,
        author: "Chris Wilson (Student)",
        text:
          "McDonald's near the city is usually open late and is a lifesaver during exam season."
      },
      {
        id: 402,
        author: "Nathan Lee (Alumni)",
        text:
          "Uber Eats is also very common here if you're studying late."
      }
    ]
  },

  {
    id: 5,
    title: "How stressful is the IT department workload?",
    author: "Sarah Mitchell (Student)",
    description:
      "I recently joined the Information Technology department and I'm curious about how stressful the workload is and how much time I should dedicate daily.",
    category: "Mentoring",
    timestamp: "Monday",
    comments: [
      {
        id: 501,
        author: "Kevin Brown (Senior Student)",
        text:
          "Generally around 2–3 hours per subject per day works well."
      },
      {
        id: 502,
        author: "Sarah Mitchell (Student)",
        text:
          "Thank you! That helps me plan my study schedule better."
      }
    ]
  },

  {
    id: 6,
    title: "Student support services on campus",
    author: "Michael Chen (Parent)",
    description:
      "Hello everyone, I was wondering what services are available on campus for student welfare, such as security, medical help, and mental health support.",
    category: "Discussion",
    timestamp: "Sunday",
    comments: [
      {
        id: 601,
        author: "Daniel Roberts (Alumni)",
        text:
          "Monash and UniMelb both have really strong student counseling services."
      },
      {
        id: 602,
        author: "Jessica Lee (Student)",
        text:
          "Campus security is also very responsive if you ever feel unsafe."
      },
      {
        id: 603,
        author: "Michael Chen (Parent)",
        text:
          "Thank you everyone for the reassurance."
      }
    ]
  }
]);

  const handleCreatePost = (newPost) => {
    const postWithId = { ...newPost, id: Date.now(), timestamp: "Just now" };
    setPosts([postWithId, ...posts]);
    setSelectedPost(postWithId);
    setIsCreating(false);
  };

  return (
    <Box
      sx={{
        backgroundColor: "background.default",
        height: "100vh",
        display: "flex",
        overflow: "hidden",
        height: "calc(100vh - 160px)"
      }}
    >
      {/* LEFT SIDEBAR */}
      <Box
        sx={{
          width: { xs: "100%", md: "400px" },
          borderRight: "1px solid",
          borderColor: "divider",
          bgcolor: "background.paper",
          overflowY: "auto",
          display: (selectedPost || isCreating) && { xs: "none", md: "block" }
        }}
      >
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
          <Box
            sx={{
              width: "100%",
              maxWidth: "800px",
              mx: "auto",
              p: { xs: 2, md: 6 }
            }}
          >
            <CreatePostView
              onCancel={() => setIsCreating(false)}
              onSubmit={handleCreatePost}
            />
          </Box>
        ) : selectedPost ? (
          <Box
            sx={{
              width: "100%",
              maxWidth: "900px",
              mx: "auto",
              p: { xs: 2, md: 6 }
            }}
          >
            <ThreadView
              key={selectedPost.id}
              post={selectedPost}
              onBack={() => setSelectedPost(null)}
            />
          </Box>
        ) : (
          <Box
            sx={{
              height: "100%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center"
            }}
          >
            <Typography
              color="text.secondary"
              variant="h5"
              sx={{ fontFamily: "Playfair Display", opacity: 0.5 }}
            >
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
