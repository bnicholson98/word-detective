"""Tests for the Team model."""

import pytest
from src.models.team import Team
from src.models.player import Player, PlayerRole
from src.models.card import CardColor


class TestTeam:
    """Test cases for Team dataclass."""
    
    def test_team_creation_valid_color(self):
        """Test team creation with valid colors."""
        red_team = Team(color=CardColor.RED)
        blue_team = Team(color=CardColor.BLUE)
        
        assert red_team.color == CardColor.RED
        assert blue_team.color == CardColor.BLUE
        assert len(red_team.players) == 0
        assert red_team.words_remaining == 0
        assert red_team.total_words == 0
    
    def test_team_creation_invalid_color(self):
        """Test team creation with invalid colors raises error."""
        with pytest.raises(ValueError, match="Team color must be RED or BLUE"):
            Team(color=CardColor.NEUTRAL)
        
        with pytest.raises(ValueError, match="Team color must be RED or BLUE"):
            Team(color=CardColor.FAILURE)
    
    def test_add_player(self):
        """Test adding players to team."""
        team = Team(color=CardColor.RED)
        chief = Player(name="Chief", role=PlayerRole.CHIEF)
        detective = Player(name="Detective", role=PlayerRole.DETECTIVE)
        
        team.add_player(chief)
        assert len(team.players) == 1
        assert team.players[0] == chief
        
        team.add_player(detective)
        assert len(team.players) == 2
        assert detective in team.players
    
    def test_get_chief(self):
        """Test getting Chief player from team."""
        team = Team(color=CardColor.BLUE)
        chief = Player(name="Chief", role=PlayerRole.CHIEF)
        detective = Player(name="Detective", role=PlayerRole.DETECTIVE)
        
        team.add_player(detective)
        team.add_player(chief)
        
        retrieved_chief = team.get_chief()
        assert retrieved_chief == chief
    
    def test_get_chief_no_chief_raises_error(self):
        """Test getting Chief when none exists raises error."""
        team = Team(color=CardColor.RED)
        detective = Player(name="Detective", role=PlayerRole.DETECTIVE)
        team.add_player(detective)
        
        with pytest.raises(ValueError, match="No Chief found on this team"):
            team.get_chief()
    
    def test_get_detectives(self):
        """Test getting Detective players from team."""
        team = Team(color=CardColor.RED)
        chief = Player(name="Chief", role=PlayerRole.CHIEF)
        detective1 = Player(name="Detective1", role=PlayerRole.DETECTIVE)
        detective2 = Player(name="Detective2", role=PlayerRole.DETECTIVE)
        
        team.add_player(chief)
        team.add_player(detective1)
        team.add_player(detective2)
        
        detectives = team.get_detectives()
        assert len(detectives) == 2
        assert detective1 in detectives
        assert detective2 in detectives
        assert chief not in detectives
    
    def test_has_chief(self):
        """Test checking if team has Chief."""
        team = Team(color=CardColor.BLUE)
        assert team.has_chief() is False
        
        detective = Player(name="Detective", role=PlayerRole.DETECTIVE)
        team.add_player(detective)
        assert team.has_chief() is False
        
        chief = Player(name="Chief", role=PlayerRole.CHIEF)
        team.add_player(chief)
        assert team.has_chief() is True
    
    def test_has_detectives(self):
        """Test checking if team has Detectives."""
        team = Team(color=CardColor.RED)
        assert team.has_detectives() is False
        
        chief = Player(name="Chief", role=PlayerRole.CHIEF)
        team.add_player(chief)
        assert team.has_detectives() is False
        
        detective = Player(name="Detective", role=PlayerRole.DETECTIVE)
        team.add_player(detective)
        assert team.has_detectives() is True
    
    def test_is_complete_team(self):
        """Test checking if team is complete."""
        team = Team(color=CardColor.BLUE)
        assert team.is_complete_team() is False
        
        chief = Player(name="Chief", role=PlayerRole.CHIEF)
        team.add_player(chief)
        assert team.is_complete_team() is False
        
        detective = Player(name="Detective", role=PlayerRole.DETECTIVE)
        team.add_player(detective)
        assert team.is_complete_team() is True
    
    def test_word_count_management(self):
        """Test word count tracking."""
        team = Team(color=CardColor.RED)
        
        team.set_word_count(8)
        assert team.total_words == 8
        assert team.words_remaining == 8
        assert team.has_won() is False
        
        team.word_found()
        assert team.words_remaining == 7
        assert team.has_won() is False
        
        for _ in range(7):
            team.word_found()
        
        assert team.words_remaining == 0
        assert team.has_won() is True
    
    def test_word_found_boundary(self):
        """Test word_found doesn't go below zero."""
        team = Team(color=CardColor.BLUE)
        team.set_word_count(1)
        
        team.word_found()
        assert team.words_remaining == 0
        
        team.word_found()
        assert team.words_remaining == 0
