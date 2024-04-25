import { render, screen } from "@testing-library/react";
import Home from "./Home";
import { BrowserRouter as Router } from "react-router-dom";

// Test for presence of welcome message
describe("Home Component", () => {
  test("renders welcome message", () => {
    render(
      <Router>
        <Home />
      </Router>
    );
    expect(screen.getByText(/Welcome to Mongo Intel/i)).toBeInTheDocument();
  });

  // Test for presence of feature sections
  test("displays the features section", () => {
    render(
      <Router>
        <Home />
      </Router>
    );
    expect(screen.getByText(/Our Features/i)).toBeInTheDocument();
    expect(screen.getByText(/Area Analysis/i)).toBeInTheDocument();
    expect(screen.getByText(/Predictive Analysis/i)).toBeInTheDocument();
  });
});

// Additional imports
import userEvent from "@testing-library/user-event";

describe("Home Component", () => {
  // Existing tests...

  // Test navigation links
  test("navigates to the correct paths when feature links are clicked", () => {
    render(
      <Router>
        <Home />
      </Router>
    );

    const links = screen.getAllByRole("link", { name: /learn more/i });
    expect(links[0]).toHaveAttribute("href", "/area-analysis");
    expect(links[1]).toHaveAttribute("href", "/predictive-analysis");
    expect(links[2]).toHaveAttribute("href", "/real-time-tracking");
  });

  // Test for specific feature descriptions
  test("displays correct descriptions for each feature", () => {
    render(
      <Router>
        <Home />
      </Router>
    );

    expect(
      screen.getByText(/Analyze geographical data over specific areas./i)
    ).toBeInTheDocument();
    expect(
      screen.getByText(/Predict future trends from historical data./i)
    ).toBeInTheDocument();
    expect(
      screen.getByText(
        /Track entities in real-time with accurate information./i
      )
    ).toBeInTheDocument();
  });

  // Test for hero section content
  test("displays correct content in the hero section", () => {
    render(
      <Router>
        <Home />
      </Router>
    );

    expect(
      screen.getByText(/Explore comprehensive tracking and analysis tools/i)
    ).toBeInTheDocument();
  });
});
