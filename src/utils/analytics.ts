/**
 * Felix Learning Platform - Learning Analytics
 * Provides analytics and insights for the learning journey
 */

export interface LearningMetrics {
  totalTimeSpent: number;
  lessonsCompleted: number;
  currentStreak: number;
  longestStreak: number;
  preferredLanguage: string;
  strongestTopic: string;
  weakestTopic: string;
  recommendedNext: string[];
}

export interface WeeklyActivity {
  week: number;
  lessonsCompleted: number;
  hoursSpent: number;
  topics: string[];
}

export class FelixAnalytics {
  private activityLog: Array<{ date: Date; phaseId: number; lessonId: string; duration: number }> = [];

  constructor() {}

  logActivity(phaseId: number, lessonId: string, durationMinutes: number): void {
    this.activityLog.push({
      date: new Date(),
      phaseId,
      lessonId,
      duration: durationMinutes,
    });
  }

  getWeeklyActivity(weeksBack: number = 4): WeeklyActivity[] {
    const now = new Date();
    const activities: WeeklyActivity[] = [];

    for (let w = 0; w < weeksBack; w++) {
      const weekStart = new Date(now);
      weekStart.setDate(now.getDate() - (w * 7));
      weekStart.setHours(0, 0, 0, 0);

      const weekEnd = new Date(weekStart);
      weekEnd.setDate(weekStart.getDate() + 7);

      const weekActivities = this.activityLog.filter(
        a => a.date >= weekStart && a.date < weekEnd
      );

      const uniqueLessons = new Set(weekActivities.map(a => a.lessonId));
      const totalTime = weekActivities.reduce((sum, a) => sum + a.duration, 0);
      const phaseIds = weekActivities.map(a => `Phase ${a.phaseId}`);
      const uniquePhases = Array.from(new Set(phaseIds));

      activities.push({
        week: weeksBack - w,
        lessonsCompleted: uniqueLessons.size,
        hoursSpent: Math.round(totalTime / 60 * 10) / 10,
        topics: uniquePhases,
      });
    }

    return activities.reverse();
  }

  calculateStreak(): { current: number; longest: number } {
    if (this.activityLog.length === 0) return { current: 0, longest: 0 };

    const dateStrings = this.activityLog.map(a => a.date.toDateString());
    const uniqueDates = Array.from(new Set(dateStrings));
    const sortedDates = uniqueDates.sort((a, b) => new Date(a).getTime() - new Date(b).getTime());

    let current = 1;
    let longest = 1;
    let temp = 1;

    for (let i = 1; i < sortedDates.length; i++) {
      const prev = new Date(sortedDates[i - 1]);
      const curr = new Date(sortedDates[i]);
      const diffDays = Math.floor((curr.getTime() - prev.getTime()) / (1000 * 60 * 60 * 24));

      if (diffDays === 1) {
        temp++;
        longest = Math.max(longest, temp);
      } else {
        if (i === sortedDates.length - 1) {
          current = temp;
        }
        temp = 1;
      }
    }

    return { current, longest };
  }

  getMetrics(): LearningMetrics {
    const streak = this.calculateStreak();
    const weekly = this.getWeeklyActivity(4);

    const totalLessons = this.activityLog.length;
    const totalTime = this.activityLog.reduce((sum, a) => sum + a.duration, 0);

    // Language preference based on most used
    const languageCounts: { [key: string]: number } = {
      'Python': 0,
      'TypeScript': 0,
      'Rust': 0,
      'Julia': 0,
    };

    // Topics distribution
    const topicCounts: { [key: string]: number } = {};

    this.activityLog.forEach(a => {
      const topic = `Phase ${a.phaseId}`;
      topicCounts[topic] = (topicCounts[topic] || 0) + 1;
    });

    const topics = Object.entries(topicCounts).sort((a, b) => b[1] - a[1]);
    const weakest = topics[topics.length - 1]?.[0] || 'None';
    const strongest = topics[0]?.[0] || 'None';

    return {
      totalTimeSpent: totalTime,
      lessonsCompleted: totalLessons,
      currentStreak: streak.current,
      longestStreak: streak.longest,
      preferredLanguage: 'Python', // Placeholder - would be calculated from actual data
      strongestTopic: strongest,
      weakestTopic: weakest,
      recommendedNext: this.getRecommendations(),
    };
  }

  private getRecommendations(): string[] {
    // Generate recommendations based on gaps in learning
    const recommendations = [
      'Complete Phase 1 Math Foundations for better DL understanding',
      'Practice implementing algorithms from scratch',
      'Review probability and statistics concepts',
    ];
    return recommendations;
  }

  generateInsights(): string[] {
    const metrics = this.getMetrics();
    const insights: string[] = [];

    if (metrics.currentStreak > 7) {
      insights.push(`🔥 Great job! You've maintained a ${metrics.currentStreak}-day learning streak!`);
    }

    if (metrics.totalTimeSpent > 300) {
      insights.push('📚 Impressive! Over 5 hours of learning recorded.');
    }

    if (metrics.weakestTopic !== 'None') {
      insights.push(`💪 Consider reviewing ${metrics.weakestTopic} - it appears to be a challenge area.`);
    }

    return insights;
  }
}

// Singleton for global use
export const felixAnalytics = new FelixAnalytics();