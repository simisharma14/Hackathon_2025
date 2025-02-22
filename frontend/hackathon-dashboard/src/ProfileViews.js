import React from "react";
import './ProfileViews.css'; // Import the CSS file
import Layout from "./Layout"; // Import Layout

const ProfileViews = () => {
  return (
    <Layout>
    <div className="view-profiles">
      <h1>View Profiles</h1>
      <p>Here you can view and manage profiles.</p>
      {/* You can add more content here */}
    </div>
    </Layout>
  );
};

export default ProfileViews;
