CREATE DATABASE AgileProjectManagement;

USE AgileProjectManagement;

CREATE TABLE Users (
    UserID INT AUTO_INCREMENT,
    Username VARCHAR(50),
    Password VARCHAR(50),
    Email VARCHAR(100),
    PRIMARY KEY(UserID)
);

CREATE TABLE Projects (
    ProjectID INT AUTO_INCREMENT,
    ProjectName VARCHAR(100),
    Description TEXT,
    StartDate DATE,
    EndDate DATE,
    UserID INT,
    PRIMARY KEY(ProjectID),
    FOREIGN KEY(UserID) REFERENCES Users(UserID)
);

CREATE TABLE Sprints (
    SprintID INT AUTO_INCREMENT,
    SprintName VARCHAR(100),
    StartDate DATE,
    EndDate DATE,
    ProjectID INT,
    PRIMARY KEY(SprintID),
    FOREIGN KEY(ProjectID) REFERENCES Projects(ProjectID)
);

CREATE TABLE Tasks (
    TaskID INT AUTO_INCREMENT,
    TaskName VARCHAR(100),
    Description TEXT,
    Status ENUM('To Do', 'In Progress', 'Done'),
    SprintID INT,
    UserID INT,
    PRIMARY KEY(TaskID),
    FOREIGN KEY(SprintID) REFERENCES Sprints(SprintID),
    FOREIGN KEY(UserID) REFERENCES Users(UserID)
);


CREATE TABLE Initiatives (
    InitiativeID INT AUTO_INCREMENT,
    InitiativeName VARCHAR(100),
    Description TEXT,
    StartDate DATE,
    EndDate DATE,
    UserID INT,
    PRIMARY KEY(InitiativeID),
    FOREIGN KEY(UserID) REFERENCES Users(UserID)
);

CREATE TABLE Epics (
    EpicID INT AUTO_INCREMENT,
    EpicName VARCHAR(100),
    Description TEXT,
    StartDate DATE,
    EndDate DATE,
    InitiativeID INT,
    UserID INT,
    PRIMARY KEY(EpicID),
    FOREIGN KEY(InitiativeID) REFERENCES Initiatives(InitiativeID),
    FOREIGN KEY(UserID) REFERENCES Users(UserID)
);

ALTER TABLE Projects ADD COLUMN EpicID INT;
ALTER TABLE Projects ADD FOREIGN KEY (EpicID) REFERENCES Epics(EpicID);

CREATE TABLE UserStories (
    StoryID INT AUTO_INCREMENT,
    StoryName VARCHAR(100),
    Description TEXT,
    Status ENUM('To Do', 'In Progress', 'Done'),
    TaskID INT,
    UserID INT,
    PRIMARY KEY(StoryID),
    FOREIGN KEY(TaskID) REFERENCES Tasks(TaskID),
    FOREIGN KEY(UserID) REFERENCES Users(UserID)
);
