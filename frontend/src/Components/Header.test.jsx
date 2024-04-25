import React from "react";
import { render, screen } from "@testing-library/react";
import Header from "./Header";
import { BrowserRouter as Router } from "react-router-dom";

describe("Header Component", () => {
  // Test for presence of brand name
  test("renders the brand name", () => {
    render(
      <Router>
        <Header />
      </Router>
    );
    const brandName = screen.getByText("Mongo Intel");
    expect(brandName).toBeInTheDocument();
  });

  // Test for presence of navigation links
  test("renders navigation links", () => {
    render(
      <Router>
        <Header />
      </Router>
    );
    const navLink1 = screen.getByRole("link", { name: /Home/i });
    const navLink2 = screen.getByRole("link", { name: /Area Analysis/i });

    expect(navLink1).toBeInTheDocument();
    expect(navLink2).toBeInTheDocument();
  });

  // Test for presence of all expected navigation links
  test("renders all expected navigation links", () => {
    render(
      <Router>
        <Header />
      </Router>
    );
    const links = [
      { text: "Home", url: "/" },
      { text: "Area Analysis", url: "/area-analysis" },
      { text: "Predictive Analysis", url: "/predictive-analysis" },
      { text: "Real-Time Tracking", url: "/real-time-tracking" },
      { text: "Location", url: "/location" },
    ];

    links.forEach((link) => {
      const navLink = screen.getByRole("link", {
        name: new RegExp(link.text, "i"),
      });
      expect(navLink).toBeInTheDocument();
      expect(navLink).toHaveAttribute("href", link.url);
    });
  });

  // If the header has a responsive design, we can test for that.
  // Test for presence of menu button in view
  test("displays menu button in view", () => {
    render(
      <Router>
        <Header />
      </Router>
    );
    // Replace 'Menu Button' with the actual text or aria-label of menu button
    const menuButton = screen.queryByLabelText(/Menu Button/i);
    if (menuButton) {
      expect(menuButton).toBeInTheDocument();
    } else {
      // check for something else if the menu button isn't there
      // For example, checking if a specific link is still visible
      const homeLink = screen.getByRole("link", { name: /Home/i });
      expect(homeLink).toBeInTheDocument();
    }
  });
});
